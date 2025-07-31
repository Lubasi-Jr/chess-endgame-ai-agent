# ♟️ Chess Endgame AI Agent

_A personalized learning tool for mastering chess endgames_

# 📖 Overview

This AI agent helps you learn chess endgames effectively by

1. Finding **relevant book pages** from "100 Endgames You Must Know"
2. Scraping strategic principles from the web
3. Generating structured lessons (with FEN positions, annotated moves, and strategies)
4. Saving lessons as PDFs and scheduling them on Google Calendar

Built using python with key libraries being **Langgraph**, **Langchain** and **Firecrawl**

---

# 🛠️ Setup

## Prerequisites

- Python version 3.10+
- Open AI API key
- Firecrawl API key
- Google Calender API credentials
- UV packahge manager. You can install it [here](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

1. Clone the repository <br><br>
   ```bash
   git clone https://github.com/Lubasi-Jr/chess-endgame-ai-agent.git
   ```
2. Install the dependecies <br><br>
   ```bash
   uv sync --locked
   ```
3. Set up your environment variables. Create a `.env` file and add: <br><br>
   ```plaintext
   OPENAI_API_KEY=your_openai_key
   FIRECRAWL_API_KEY=your_firecrawl_key
   GOOGLE_CALENDAR_CREDENTIALS=path/to/credentials.json
   ```

---

# 🚀 Usage

Run the agent with <br>

```bash
   uv run main.py --topic '[Your endgame topic]'
```

## What happens?

1. **Book extraction**: Finds the relevant pages from the book '100 Endgames you must know' which is in the `/resources` folder
2. **Web scraping**: Agent scrapes the web to find principles about that particular topic. All the markdown from the websites scraped is parsed to an llm to create a standarised set of principles
3. Lesson generation: Creates PDF's with <br>

- FEN position
- Annotated moves
- Strategic explanations

4.  **Scheduling**: Adds lessons tasks to your Google Calender so that you are reminded to keep learning
