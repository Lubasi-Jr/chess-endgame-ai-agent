class DeveloperToolsPrompts:
    """Collection of prompts for analyzing developer tools and technologies"""

    
    # System prompt
    ENDGAME_LOCATOR_SYSTEM = """You are a chess book researcher assistant. Your job is to read a Table of Contents from a chess book and identify where a given endgame topic appears in the book.

You must also generate a helpful web search query for finding external resources (like rules, tips, or tutorials) on how to play that specific endgame.

Your final output must follow this format:

<start_page>
<end_page>
<search_query>
"""
    @staticmethod
    def endgame_locator_user(topic: str, table_of_contents: str) -> str:
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
    
    @staticmethod
    def next_function():
        pass