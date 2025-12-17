# ♟️ Chess Endgame AI Agent

An intelligent chess endgame tutor powered by AI that generates personalized lessons from the acclaimed book _"100 Endgames You Must Know"_ by Jesús de la Villa. This agent combines book knowledge with web-scraped principles to create comprehensive PDF lessons tailored to your chosen endgame topic.

## About

The Chess Endgame AI Agent is a LangGraph-powered workflow that helps chess players master critical endgame positions. When you provide an endgame topic (such as "King and Pawn vs King" or "Rook Endgames"), the agent:

1. **Locates relevant pages** from the "100 Endgames You Must Know" book using AI-powered table of contents analysis
2. **Extracts content** from the identified book sections
3. **Searches the web** using Firecrawl to gather additional endgame principles and strategies
4. **Generates structured rules** by synthesizing book content with web-sourced knowledge
5. **Creates PDF lessons** complete with FEN positions, strategic goals, move sequences and links to the underlying principles

The result is a collection of downloadable PDF lessons saved to your `lessons` folder, ready for study.

## Installation

### Prerequisites

Before installing the Chess Endgame AI Agent, ensure you have the following installed on your system:

| Requirement                 | Version | Download Link                                                                |
| --------------------------- | ------- | ---------------------------------------------------------------------------- |
| Python                      | 3.10+   | [python.org/downloads](https://www.python.org/downloads/)                    |
| uv (Python package manager) | Latest  | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| Git                         | Latest  | [git-scm.com/downloads](https://git-scm.com/downloads)                       |

### Step 1: Clone the Repository

Open your terminal and run the following commands:

```bash
git clone https://github.com/Lubasi-Jr/chess-endgame-ai-agent.git
```

Navigate into the project directory:

```bash
cd chess-endgame-ai-agent
```

### Step 2: Open in Your Code Editor

Open the project in Visual Studio Code (or your preferred editor):

```bash
code .
```

### Step 3: Install Dependencies

With `uv` installed, run the following command to install all required packages:

```bash
uv sync
```

This will read the `pyproject.toml` file and install all dependencies into a virtual environment.

### Step 4: Configure Environment Variables

Create a `.env.local` file in the root of the project:

```bash
touch .env.local
```

Open the file and add the following environment variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

#### Getting Your API Keys

**OpenAI API Key:**

1. Visit [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to **API Keys** in the left sidebar
4. Click **Create new secret key**
5. Copy the key and paste it into your `.env.local` file

**Firecrawl API Key:**

1. Visit [firecrawl.dev](https://www.firecrawl.dev/)
2. Sign up for an account
3. Navigate to your dashboard
4. Copy your API key and paste it into your `.env.local` file

### Step 5: Run the Application

Start the Chess Endgame AI Agent by running:

```bash
uv run python main.py
```

You can also pass a topic directly as a command-line argument:

```bash
uv run python main.py --topic "King and Pawn vs King"
```

## Usage

Once the application starts, you will see:

```
CHESS ENDGAME TEACHER AGENT
What Endgame do you want to study?:
```

Enter your desired endgame topic (for example):

- `King and Pawn vs King`
- `Rook and Pawn Endgames`
- `Queen vs Rook`
- `Bishop Endgames`
- `Lucena Position`

The agent will then:

1. Search the book's table of contents for relevant pages
2. Extract the book content
3. Search the web for additional principles
4. Generate structured lessons
5. Save PDF files to the `lessons` folder

When complete, you will see:

```
💾 PDF saved as lesson1.pdf
💾 PDF saved as lesson2.pdf
All the best with your learning!!
```

Navigate to the `lessons` folder to find your generated PDF lessons.

## Troubleshooting

### Common Issues and Solutions

**"ModuleNotFoundError: No module named 'xxx'"**

Ensure you have installed all dependencies:

```bash
uv sync
```

**"OPENAI_API_KEY not found" or "FIRECRAWL_API_KEY not found"**

Make sure your `.env.local` file exists in the project root and contains valid API keys. Also ensure `load_dotenv()` is loading the correct file. You may need to rename it to `.env`:

```bash
mv .env.local .env
```

**"Rate limit exceeded" errors**

You may have exceeded your API quota. Check your usage at:

- OpenAI: [platform.openai.com/usage](https://platform.openai.com/usage)
- Firecrawl: Your Firecrawl dashboard

Consider waiting a few minutes before retrying.

**PDF files not appearing in the lessons folder**

Ensure the `lessons` folder exists. If not, create it:

```bash
mkdir lessons
```

**"No book content found" or empty lessons**

The topic you entered may not match content in the book's table of contents. Try using more specific chess terminology such as:

- "Pawn Endgames"
- "Rook Endgames"
- "Minor Piece Endgames"

**Windows-specific path issues**

If you encounter path-related errors on Windows, ensure you are using forward slashes or raw strings in any custom path configurations.

### Still Having Issues?

1. Check that your Python version is 3.10 or higher: `python --version`
2. Ensure `uv` is properly installed: `uv --version`
3. Try deleting the `.venv` folder and reinstalling: `rm -rf .venv && uv sync`
4. Open an issue on the [GitHub repository](https://github.com/Lubasi-Jr/chess-endgame-ai-agent/issues)

## Contributing

Contributions are welcome! Whether it's bug fixes, new features or documentation improvements, your input helps make this project better.

### How to Contribute

1. **Fork the repository**

   Click the "Fork" button at the top right of the [repository page](https://github.com/Lubasi-Jr/chess-endgame-ai-agent).

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/chess-endgame-ai-agent.git
   cd chess-endgame-ai-agent
   ```

3. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**

   Implement your feature or bug fix. Ensure your code follows the existing style and includes appropriate comments.

5. **Test your changes**

   Run the application to verify everything works:

   ```bash
   uv run python main.py --topic "King and Pawn vs King"
   ```

6. **Commit your changes**

   Write clear, descriptive commit messages:

   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

7. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**

   Go to the original repository and click "New Pull Request". Select your fork and branch, then provide a clear description of your changes.

### Contribution Ideas

- Add support for additional chess books
- Implement alternative LLM providers (Anthropic Claude, Google Gemini)
- Create a web interface for the agent
- Add spaced repetition scheduling for lessons
- Improve PDF formatting and styling
- Add support for PGN file generation
- Write unit tests for the workflow components

---

**Built by Lubasi Milupi**

_Master the endgame. Master the game._
