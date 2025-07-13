from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from .book import BookUtilities
from .prompts import Prompts
from .firecrawl import FirecrawlService
from .models import EndgameState
from typing import List, Optional, Dict, Any

load_dotenv()

class Workflow:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.firecrawl = FirecrawlService()
        self.prompt = Prompts()
        self.book = BookUtilities()

    # Step 1
    def _read_book_step(self, state: EndgameState) -> Dict[str,Any]:
        
        try:
            # Firstly, determine what pages are required
            table_of_contents = self.book.get_table_of_contents()
            messages = [SystemMessage(content= self.prompt.PAGE_LOCATOR_SYSTEM), HumanMessage(content= self.prompt.page_locator_user(state.topic,table_of_contents))]
            print('📖♟️Finding what pages in the "100 Endgames you should know" book by "Jesus De La Villa" are needed to give you these lessons')
            response = self.llm.invoke(messages)
            output = response.content.strip().splitlines()
            start_page = output[0]
            end_page = output[1]
            search_query = output[2]
            # Now that pages are found, extract the book
            print(f'💡Pages found are {start_page} and {end_page}. Currently extracting information from the book')
            book_extract = self.book.get_book_extract(start_page,end_page)
            content = book_extract.text_content
            pages = book_extract.image_blocks
            return {"piece_query": search_query, "book_text_content": content, "book_pages": pages}
        except Exception as e:
            print(e)
            return {"piece_query": 'How to play Endgames like Magnus Carlsen', "book_text_content": 'An error occurred, No book content', "book_pages": []}
        
    # Helper function to scrape the web
    def _web_scraper(self, query: str) -> str:
        try:
            print(f'🔎Searching the web to find specific Endgame principles. Query used is {query}')
            search_results = self.firecrawl.search_for_rules(query,4)
            all_content = ''
            for data in search_results.data:
                url = data.get('url','')
                scraped = self.firecrawl.scrape_websites(url)
                if scraped:
                    all_content += scraped.markdown[:1550] + "\n\n"
            return all_content

        except Exception as e:
            print(e)
            return 'No content from the web, and error occured while attempting to scrape. Please use your own knowledge about Chess Endgames'
    # Step 2
    def _generate_rules_step(self, state: EndgameState) -> Dict[str, Any]:
        # Use firecrawl to search the web
        web_content = self._web_scraper(state.piece_query)
        # Web has been scraped, use the LLM to generate principles
        try:
            messages = [SystemMessage(content=self.prompt.RULE_GENERATOR_SYSTEM), HumanMessage(content=self.prompt.rule_generator_user(state.piece_query, web_content))]
            print('📜Using the LLM to generate specific rules and principles from the scraped content')
            result = self.llm.invoke(messages)
            principles = result.content.strip()
            return {"piece_rules": principles}

        except Exception as e:
            print(e)
            return {'piece_rules': '1. No rules generated, an error occurred\n2. I repeat, no rules generated. Come up with your own shame'} 
        
    # Step 3
    def _lesson_generation(self, state: EndgameState) -> Dict[str, Any]:
        pass
        
            