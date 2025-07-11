from langchain_core.messages import SystemMessage, HumanMessage

class Prompts:
    """Collection of prompts for assissting the AI agent with the task of providing endgame lessons"""

    # Prompts for determining which page from the 100 endgames book to extract information from
    PAGE_LOCATOR_SYSTEM = """You are a chess book researcher assistant. Your job is to read a Table of Contents from a chess book and identify where a given endgame topic appears in the book.

    You must also generate a helpful web search query for finding external resources (like rules, tips, or tutorials) on how to play that specific endgame.

    Your final output must follow this format:

    <start_page>
    <end_page>
    <search_query>
    """
    @staticmethod
    def page_locator_user(topic: str, table_of_contents: str) -> str:
        return f"""A chess student wants to study the following topic:

                "{topic}"

                Here is the full Table of Contents of the book (note: page numbers in this TOC are 1-indexed):

                {table_of_contents}

                Your task:
                1. Identify which section(s) most closely match the topic
                2. Determine the **start** and **end** page numbers (convert to 0-indexed format)
                3. Generate a simple, natural-sounding Google-style search query (e.g., "how to play bishop and knight endgames")

                Rules:
                - Return exactly three lines:
                - First line: 0-indexed start page (e.g., page 21 → 20)
                - Second line: 0-indexed end page
                - Third line: Search query string (e.g., "how to play rook and bishop endgames")
                - Do **not** return anything else
                - The query must match the user’s topic and be useful for scraping instructional material from the web

                Example output:
                20
                34
                how to play rook and bishop endgames
                """
    
    # These prompts below are for generating instructional rules from scraped chess endgame content (Scraped from the web using firecrawl).
    RULE_GENERATOR_SYSTEM = """
    You are a professional chess coach and writer.

    Your job is to read long-form instructional content about a specific chess endgame and extract 5 to 10 clear, actionable rules or principles that a student should follow when playing that endgame.

    Each rule must be:
    - Numbered (1., 2., etc.)
    - Written in a concise, imperative style (e.g., "Bring your king to the center early")
    - Based only on the information in the content provided

    Do not add introductions, explanations, or summaries. Output only the numbered rules.

    Example format:

    1. Always aim to bring your king toward the center early.  
    2. Use opposition to restrict the enemy king's movement.  
    3. Do not push the pawn until your king is in front of it.  
    4. Understand and apply the "square rule" to judge pawn promotion potential.  
    5. Use shouldering techniques to block the opposing king.  
    6. In critical positions, calculate whether promotion can be forced before pushing.  
    7. Avoid stalemating positions near the promotion square.  
    8. Keep your king in front of the pawn when advancing.  
    9. Force the enemy king to the edge before pushing the pawn.  
    10. Know basic winning and drawing techniques in king and pawn vs king endgames.
    """

    @staticmethod
    def rule_generator_user(search_query: str, scraped_content: str) -> str:
        return f"""
        Based on the Students request, the search query used was: **{search_query}**

        Based on the instructional material below, extract 5 to 10 clear rules or principles that they can follow to play the particular endgame well.

        Only output the rules — no headings, commentary, or explanations.

        Scraped Content:
        {scraped_content}
                """
    # Prompts for generating endgame lessons using the rules generated, content from the book as well as actual pages images
    LESSON_GEN_SYSTEM = SystemMessage(
        content=(
            "You are a chess tutor. Given images and text from a chess endgame book, "
            "explain the board positions, give insights, and convert them into PGN if possible."
        )
    )

    @staticmethod
    def lesson_gen_user(topic: str, text_content: str, image_blocks: list) -> HumanMessage:
        return HumanMessage(content=[
            {"type": "text", "text": f"Please analyze the following chess endgame material related to: {topic}. "
                                     "Explain the positions based on the diagrams and text, provide PGN if possible, "
                                     "and summarize the key principles or strategies."},
            {"type": "text", "text": text_content},
            *image_blocks
        ])
