from typing import List, Optional, Dict, Any
from pydantic import BaseModel

"""Structured output for LLM company analysis focused on developer tools"""

class EndgameState(BaseModel):
    """State that will be used in the graph by Langgraph"""
    topic: str
    general_query: str 
    piece_query: str
    endgame_rules: str
    piece_rules: str
    book_text_content: str
    book_pages: List[Any]
    Lessons: Any


