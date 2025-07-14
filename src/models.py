from typing import List, Optional, Dict, Any, Hashable
from pydantic import BaseModel



class ChessLesson(BaseModel):
    """Structured output for LLM company analysis focused on developer tools"""
    title: List[str]
    situation: List[str]
    FEN: List[str]
    goal: List[str]
    strategy: List[str]
    moves: List[str]
    rules_link: List[str]

class EndgameState(BaseModel):
    topic: str
    piece_query: Optional[str] = None
    piece_rules: Optional[str] = None
    book_text_content: Optional[str] = None
    book_pages: Optional[List[Any]] = None
    lessons: Optional[Dict[str, List[str]]] = None


