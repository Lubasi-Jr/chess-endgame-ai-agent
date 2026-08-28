# Chess Endgame AI Agent

An AI agent that generates personalised chess endgame lessons on demand. Give it a topic like "King and Pawn vs King" or "Rook Endgames" and it locates the relevant pages in a reference book, researches supplementary principles on the web, synthesises them, and produces a pack of downloadable PDF lessons complete with FEN positions, strategic goals, and annotated move sequences.

This repository is the **backend**: a FastAPI service wrapping a LangGraph agent pipeline. A separate [React frontend](https://github.com/Lubasi-Jr/chess-endgame-ai-agent-frontend) provides a web UI on top of it. The backend can also be run as a standalone CLI tool.

> **Status:** personal project. It runs end to end, but it is not production-hardened. See [Limitations](#limitations) for an honest account of what is and isn't handled.

## How it works

The core is a four-stage [LangGraph](https://langchain-ai.github.io/langgraph/) `StateGraph`, where each node is a pure function over a typed Pydantic state object:

1. **`read`** — An LLM (`gpt-4o-mini`) reads the reference book's table of contents alongside your free-text topic and returns the exact page range to extract, plus a web search query. The identified pages are then pulled from the bundled book PDF using PyMuPDF, extracting both the page text and a rendered image of each page.
2. **`rules`** — [Firecrawl](https://www.firecrawl.dev/) searches the web for the generated query, scrapes the top results, and the LLM synthesises the content into a concise list of endgame principles.
3. **`lesson`** — The topic, synthesised principles, extracted book text, and the book page images are combined into a single multimodal prompt. The LLM returns several complete, structured lessons in one call, validated against a Pydantic schema.
4. **`pdf`** — Each lesson is rendered to a PDF. The backend zips them and streams the archive back to the caller.

Two design choices worth calling out:

- **Multimodal grounding.** Rather than feeding the model only extracted text, the located book pages are rasterised to images and sent alongside the text, so the model can reason over the book's actual diagrams and positions.
- **LLM-as-router.** Instead of hand-written table-of-contents matching, the model reads the ToC and decides which pages are relevant, letting semantic matching replace a brittle keyword algorithm.

## Tech stack

| Area | Tooling |
| --- | --- |
| Language / runtime | Python 3.10+ |
| Package management | [uv](https://docs.astral.sh/uv/) (with committed lockfile) |
| Web framework | FastAPI, served via Uvicorn |
| Agent orchestration | LangGraph, LangChain |
| LLM | OpenAI `gpt-4o-mini` (via `langchain-openai`) |
| Web search / scraping | Firecrawl |
| Book PDF parsing | PyMuPDF (`fitz`) |
| PDF generation | `fpdf` |
| Data validation | Pydantic v2 |
| Containerisation | Docker |

## Getting started

### Prerequisites

| Requirement | Version | Link |
| --- | --- | --- |
| Python | 3.10+ | [python.org/downloads](https://www.python.org/downloads/) |
| uv | Latest | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| Git | Latest | [git-scm.com/downloads](https://git-scm.com/downloads) |

### 1. Clone and install

```bash
git clone https://github.com/Lubasi-Jr/chess-endgame-ai-agent.git
cd chess-endgame-ai-agent
uv sync
```

`uv sync` reads `pyproject.toml` and installs all dependencies into a virtual environment.

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
```

- **OpenAI key:** [platform.openai.com](https://platform.openai.com/) → API Keys → Create new secret key.
- **Firecrawl key:** [firecrawl.dev](https://www.firecrawl.dev/) → sign up → copy your key from the dashboard.

Both keys are required. The service reads them at startup and calls out to OpenAI and Firecrawl on every request, so generating lessons consumes credits on both.

## Running the backend

### As an HTTP API (used by the frontend)

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 8000
```

The API is then available at `http://localhost:8000`.

### As a CLI tool (no server)

```bash
uv run python main.py --topic "King and Pawn vs King"
```

Or run it interactively and enter a topic when prompted:

```bash
uv run python main.py
```

Generated PDFs are written to the `lessons/` folder.

### With Docker

```bash
docker build -t chess-endgame-agent .
docker run -p 8000:8000 --env-file .env chess-endgame-agent
```

## API reference

### `GET /health`

Liveness check. Returns:

```json
{ "status": "ok", "message": "Chess Endgame AI Agent is running" }
```

### `POST /lessons`

Generates lessons for a topic and returns them as a ZIP archive of PDFs.

**Request body:**

```json
{ "query": "Rook Endgames" }
```

**Response:** a binary `application/zip` stream (`Content-Disposition: attachment`) containing one PDF per generated lesson. The request runs the full agent pipeline synchronously, so it blocks until every lesson is generated; expect it to take a little time while the LLM and web-scraping calls complete.

**Errors:** `400` for an empty query, `422` for a malformed body, `500` for a generation failure.

## Connecting the frontend

The [frontend](https://github.com/Lubasi-Jr/chess-endgame-ai-agent-frontend) reads its backend URL from a `VITE_API_URL` environment variable at build time. Point it at wherever this backend is running (for local development, `http://localhost:8000`). CORS is currently open to all origins to keep local development simple.

## Project structure

```
app.py              FastAPI app and HTTP entrypoint
main.py             CLI entrypoint (drives the same workflow without HTTP)
src/
  workflow.py       LangGraph pipeline definition and orchestration
  models.py         Pydantic schemas (graph state, lesson output schema)
  book.py           Book PDF / table-of-contents extraction (PyMuPDF)
  firecrawl.py      Firecrawl web search + scraping wrapper
  prompts.py        Prompt templates
  pdf.py            Lesson-to-PDF rendering (fpdf)
  calender.py       Google Calendar scheduling (built, currently disabled)
resources/          Bundled reference book and extracted table of contents
```

## Limitations

This is a personal project and is deliberately honest about its rough edges:

- **Synchronous requests.** `POST /lessons` runs the whole pipeline inline and can take a while; there is no background job queue or progress streaming.
- **No request isolation.** Generated PDFs are written to a single shared `lessons/` folder, so concurrent requests can interfere with each other. Fine for single-user local use, not for concurrent load.
- **Minimal hardening.** No authentication, no rate limiting, open CORS, and no retry-with-backoff on the LLM or scraping calls (each gets one attempt with a graceful fallback).
- **No automated tests or CI** yet.
- **Calendar scheduling is disabled.** The Google Calendar node is fully written but commented out of the active graph.

## Roadmap

Natural next steps, several of which double as good contributions:

- Offload generation to a background task queue with a job-status endpoint the frontend can poll.
- Give each request an isolated working directory to remove the concurrency race.
- Add schema-level validation on the multi-lesson output and a retry-with-correction loop.
- Support alternative LLM providers (Anthropic Claude, Google Gemini) and additional reference books.
- Add a JSON lesson endpoint so the frontend can render lessons in-page instead of only offering a download.
- Add unit tests for the workflow nodes and a CI pipeline.

## Contributing

Contributions are welcome, bug fixes, features, or documentation. Fork the repo, create a feature branch, make your changes, and open a pull request with a clear description.

---

**Built by Lubasi Milupi**

_Master the endgame. Master the game._