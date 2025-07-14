from langchain_core.messages import SystemMessage, HumanMessage

class LessonGeneratorPrompts:
    """Prompts for explaining chess endgames using book content and diagrams"""

    SYSTEM_MESSAGE = SystemMessage(
        content=(
            "You are a chess tutor. Given images and text from a chess endgame book, "
            "explain the board positions, give insights, and convert them into PGN if possible."
        )
    )

    @staticmethod
    def get_system_lesson_gen_prompt(topic: str) -> SystemMessage:
        SYSTEM_MESSAGE = SystemMessage(content=f"""You are a chess grandmaster creating detailed endgame lessons for an intermediate player. 
            The student prefers thorough explanations in simple English with carefully limited chess notation.

            Your task is to create comprehensive lessons based on:
            1. The endgame topic: {topic}
            2. Key principles obtained from scraping the web on that topic:
            3. Relevant content from '100 Endgames book by Jesus De La Villa'

            IMPORTANT INSTRUCTIONS:
            - Create multiple complete lessons (typically 3-5)
            - Each lesson must follow EXACTLY this 7-field structure:
            * Title: Numbered lesson with specific scenario
            * Situation: Detailed plain English description
            * FEN: Exact position in FEN notation
            * Goal: Clear objectives for both sides
            * Strategy: Comprehensive winning plan
            * Moves: Step-by-step guidance ending with notation
            * Rules Link: All relevant principle connections

            EXAMPLE FORMAT:
            Title: "Lesson 1: King and Pawn vs. King - Shouldering Technique"
            Situation: "Your white king stands on e4 with a pawn on e5. The black king approaches from the side on f7. You need to prevent the black king from reaching the pawn's queening square while advancing your own king to create space."
            FEN: "8/5k2/8/4P3/4K3/8/8/8 w - - 0 1"
            Goal: "Promote the pawn while preventing the black king from blocking its path. Black aims to reach e8 or g8 to stop the pawn."
            Strategy: "Use the 'shouldering' technique where your king moves diagonally to cut off the enemy king. First prevent the black king from approaching directly, then advance your pawn when the path is clear. The key is maintaining the opposition while making progress."
            Moves: "First move your king to f5 to block the black king's direct path. If they respond with Kf8, advance to e6 controlling key squares. The most accurate move order would be: 1. Kf5 Kf8 2. Ke6 Ke8 3. e6 Kd8 4. Kf7"
            Rules Link: "This demonstrates Principle 2 (King activity) as your king actively cuts off the opponent. It also shows Principle 5 (Opposition) in the final moves, and Principle 7 (Pawn advancement timing) regarding when to push the pawn."
            """)
        return SYSTEM_MESSAGE

    @staticmethod
    def get_user_lesson_gen_prompt(topic: str, principles: str, text_content_from_book: str, image_blocks: list) -> HumanMessage:
        USER_PROMPT = f"""Create thorough endgame lessons about {topic} using these principles:
            {principles}

            Book content to use:
            {text_content_from_book}

            The actual pages of this book have been uploaded as images as part of this prompt so do have a look in order to gain a complete understanding

            Required Output Format:
            - List of ChessLesson objects (3-5 complete lessons. The number of lessons depend on how many lessons are described in the book). Keep note that the ChessLesson class is as follows:

            class ChessLesson(BaseModel):
            #Structured output for LLM company analysis focused on developer tools
                title: List[str]
                situation: List[str]
                FEN: List[str]
                goal: List[str]
                strategy: List[str]
                moves: List[str]
                rules_link: List[str]
            Since you are using this as a structured output I would like that each element of the lesson would be placed in the appropriate index of the array attribute. For example, title[0] should conatin the title for lesson 1 and title[1] should contain the title for lesson 2 and so on and so forth for all the other lessons

            - All fields must contain detailed paragraphs (3-4 sentences)
            -'moves' field must include:
            * English description of key moves
            * Final line with precise notation
            - FEN must exactly match described positions

            Critical Guidelines:
            1. Length & Detail:
            - NO 1-sentence answers anywhere
            - Situation: 3-4 sentences describing the position
            - Strategy: 4-5 sentences explaining the plan
            - Moves: 3 sentences + notation line
            - Rules Link: Must mention ALL relevant principles

            2. Notation Rules:
            - Only in FEN and final moves line
            - Precede notation with: "The most accurate move order would be:"
            - Use simple algebraic (e.g., "Nf3" not "Ng1-f3")

            3. Principle Linking:
            - If multiple principles apply, mention ALL of them
            - Explain how each principle applies to the position
            - Never say "this demonstrates Principle X" without explanation

            Remember:
            1. The student wants to deeply understand these positions
            2. Every explanation should be worth reading - no fluff
            3. Connect concepts to practical play
            4. Use chess terms only when absolutely necessary
            5. Imagine you're explaining to someone who knows basics but gets overwhelmed by dense chess literature
            """ 
        return HumanMessage(content=[
            {"type": "text", "text": USER_PROMPT},
            *image_blocks
        ])

class RuleDefinePrompts:
    peak ='PEAK STILL'

class TableOfContentsPrompts:
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
    


class EndgameRulesPrompts:
    """Prompts for generating instructional rules from scraped chess endgame content."""

    # System prompt for the assistant
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
    

    # Lesson generator
    SYSTEM_PROMPT = """You are a chess grandmaster creating detailed endgame lessons for an intermediate player. 
The student prefers thorough explanations in simple English with carefully limited chess notation.

Your task is to create comprehensive lessons based on:
1. The endgame topic: {topic}
2. Key principles: {principles}
3. Relevant content from '100 Endgames': {text_content_from_book}

IMPORTANT INSTRUCTIONS:
- Create multiple complete lessons (typically 3-5)
- Each lesson must follow EXACTLY this 7-field structure:
  * Title: Numbered lesson with specific scenario
  * Situation: Detailed plain English description
  * FEN: Exact position in FEN notation
  * Goal: Clear objectives for both sides
  * Strategy: Comprehensive winning plan
  * Moves: Step-by-step guidance ending with notation
  * Rules Link: All relevant principle connections

EXAMPLE FORMAT:
Title: "Lesson 1: King and Pawn vs. King - Shouldering Technique"
Situation: "Your white king stands on e4 with a pawn on e5. The black king approaches from the side on f7. You need to prevent the black king from reaching the pawn's queening square while advancing your own king to create space."
FEN: "8/5k2/8/4P3/4K3/8/8/8 w - - 0 1"
Goal: "Promote the pawn while preventing the black king from blocking its path. Black aims to reach e8 or g8 to stop the pawn."
Strategy: "Use the 'shouldering' technique where your king moves diagonally to cut off the enemy king. First prevent the black king from approaching directly, then advance your pawn when the path is clear. The key is maintaining the opposition while making progress."
Moves: "First move your king to f5 to block the black king's direct path. If they respond with Kf8, advance to e6 controlling key squares. The most accurate move order would be: 1. Kf5 Kf8 2. Ke6 Ke8 3. e6 Kd8 4. Kf7"
Rules Link: "This demonstrates Principle 2 (King activity) as your king actively cuts off the opponent. It also shows Principle 5 (Opposition) in the final moves, and Principle 7 (Pawn advancement timing) regarding when to push the pawn."
"""


