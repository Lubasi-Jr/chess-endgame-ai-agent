from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.endgame import BookUtilities
from src.prompts import DeveloperToolsPrompts
from src.models import EndgameState
import json

load_dotenv()

prompter = DeveloperToolsPrompts()


topic = 'I want to learn Rook vs 2 Pawns Endgame'
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
    print(book)
    # Prompt LLM with book pages and text content
    messageBlock = [
    SystemMessage(content="You are a chess tutor. Given images and text from a chess endgame book, explain the board positions, give insights, and convert them into PGN if possible."),
    HumanMessage(content=[
        {"type": "text", "text": "Please analyze the following chess endgame material and explain the positions. Provide PGN if possible and offer general principles or strategies."},
        {"type": "text", "text": book.text_content},
        *book.image_blocks  
    ])]
    result = llm.invoke(messageBlock)
    print('🔎LLM is analysing text content and images from the book')
    print('💡Analysis below')
    print()
    print(result.content)


except Exception as e:
    print("An error occured:")
    print(e)


