from typing import List, Optional, Dict, Any
from pydantic import BaseModel



class ChessLesson(BaseModel):
    """Structured output for LLM company analysis focused on developer tools"""
    title: str
    situation: str
    FEN: str
    goal: str
    strategy: str
    moves: str
    rules_link: str

class EndgameState(BaseModel):
    """State that will be used in the graph by Langgraph"""
    topic: str
    piece_query: str
    piece_rules: str
    book_text_content: str
    book_pages: List[Any]
    #Lessons: Any


""" You are a chess grandmaster that is giving endgame lessons to this intermediate player. They questioned you on the topic {}
    and you did some research on principles they should follow. The principles are as follows:
    {}
    You also did read content from the book 100 Endgames and extracted the following text and pages:
    Above is the text from the relevant pages needed for the topic asked, the actual pages have been attached as images for you to look at. 
    Using this info from the book and the rules I would like you to come up with a list of lessons for the student. The number of lessons will be dependant on the number of lessons that are brought up in the book.
    Each lesson has the following structure
    title: The name of the lesson and its number. E.g Lesson 2.1: Rook and Knight Endgame- Knight on g7 or b7
    situation: This is the current board situation and position that you tell the student. Keep in mind to use simple English here, that is what the student prefers. They dislike having to use Chess Notation and too much chess jargon as is present in the book. That is why the find the book hard to use and therefore need your assistance. Describe the board situation of this lesson precicely and easy for them to understand. An example would be you telling them that the king is infront of its pawn and the opponents kind is 1 square from them, instead of saying that they are in opposition
    FEN: this is an FEN string of the board situation described earlier. The student can use this string, paste it into an analysis board and begin praciticing that position
    goal: Describe the goal of the position and what the chess player aims to achieve
    strategy: Describe how they reach this goal, what moves they should play. Try to not use too much chess notation but rather just tell them the moves using English. For example in a king pawn endgame where the king is on c4 with the pawn on d4 the king has to make a move that controls either c6, d6, e6 (The critical squares for the pawn). Now instead of using chess notation just tell the student they must make a move that gives the king control of one of the 3 squares that are 2 ranks in front of the pawn. 
    rules_link: This last attribute just describes how the moves in this position link back to some (or all) of the principles stated above, with proper descriptions of the link

    Just a reminder that you must return a list of these lessons, I will loop through each lesson and create a text file for my student for each lesson.
    """
