from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.book import BookUtilities
from src.prompt_testing import TableOfContentsPrompts, EndgameRulesPrompts, LessonGeneratorPrompts
from src.models import EndgameState, ChessLesson
import json
from src.firecrawl import FirecrawlService
from typing import List

load_dotenv()

prompter = TableOfContentsPrompts()
firecrawl = FirecrawlService()


topic = 'I want to learn king and pawn only Endgames'
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
table_of_contents = BookUtilities.get_table_of_contents()
messages = [SystemMessage(content=prompter.ENDGAME_LOCATOR_SYSTEM), HumanMessage(content=prompter.endgame_locator_user(topic,table_of_contents))]

try:
    response = llm.invoke(messages)
    output = response.content.strip().splitlines()
    start_page = int(output[0])
    end_page = int(output[1])
    search_query = output[2]
    print(f"Pages required for this topic are {start_page} and {end_page}. Performing extracton...")
    print(f"The topic that is to be used to scrape the web is : {search_query}")
    
    book = BookUtilities.get_book_extract(start_page,end_page)

    # Test out Firecrawl
    print('🔎 Searching firecrawl to discover rules')
    search_results = firecrawl.search_for_rules(search_query)
    all_content = ""
    for result in search_results.data:
        url = result.get('url',"")
        scraped = firecrawl.scrape_websites(url=url)
        if scraped:
            all_content += scraped.markdown[:1550] + "\n\n"
    # Query the llm with the information from firecrawl
    ruleObject = EndgameRulesPrompts()
    ruleMessages = [SystemMessage(content=ruleObject.RULE_GENERATOR_SYSTEM), HumanMessage(content=ruleObject.rule_generator_user(search_query,all_content))]
    print('🖊️ Generating rules using data from firecrawl')
    result = llm.invoke(ruleMessages)
    rulesGenerated = result.content.strip()
    # Generate Lessons
    lessonGen = LessonGeneratorPrompts()
    human = lessonGen.get_user_lesson_gen_prompt(topic,rulesGenerated,book.text_content,book.image_blocks)
    system = lessonGen.get_system_lesson_gen_prompt(topic)
    messageBlock = [system,human]
    structured_llm = llm.with_structured_output(ChessLesson)
    print('🖊️ Generating Lessons')
    response = structured_llm.invoke(messageBlock)
    print('Done generating the lessons')
    hashmap = {key: value for key, value in response}
    print(f'Rules Link for lesson 2 is {hashmap["rules_link"][0]}')
        
    



    

   






except Exception as e:
    print("An error occured:")
    print(e)


