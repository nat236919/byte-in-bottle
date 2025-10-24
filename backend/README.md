# Byte in Bottle - Backend

> Powered by bytes. Driven by attitude.

FastAPI backend with Ollama integration for AI-powered chat and text generation.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🤖 **Ollama Integration** - Local LLM support with Ollama
- ⚡ **UV Package Manager** - Lightning-fast Python package management by Astral
- 🔄 **CORS Enabled** - Ready for frontend integration
- 📝 **Auto-generated Docs** - Interactive API documentation with Swagger UI

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Ollama](https://ollama.ai/) - Install and have it running locally

## Quick Start

1. **Install dependencies:**

   ```bash
   uv sync
   ```

2. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

3. **Ensure Ollama is running:**

   ```bash
   # Pull a model (if you haven't already)
   ollama pull llama3.2
   ```

4. **Run the server:**

   ```bash
   # Using uv
   uv run backend
   
   # Or directly with uvicorn
   uv run uvicorn backend.main:app --reload
   ```

5. **Access the API:**
   - API: <http://localhost:8000>
   - Interactive docs: <http://localhost:8000/docs>
   - ReDoc: <http://localhost:8000/redoc>

## API Endpoints

### Health Check

```bash
GET /health
```

### List Models

```bash
GET /models
```

### Chat Completion

```bash
POST /chat
Content-Type: application/json

{
  "model": "llama3.2",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}
```

### Text Generation

```bash
POST /generate?model=llama3.2&prompt=Hello!
```

## Development

```bash
# Run with auto-reload
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Add new dependencies
uv add <package-name>

# Update dependencies
uv sync
```

## Project Structure

```raw
backend/
├── src/
│   └── backend/
│       ├── __init__.py
│       └── main.py          # FastAPI application
├── .env.example             # Environment variables template
├── .gitignore
├── pyproject.toml           # Project configuration
└── README.md
```

## Environment Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `ALLOWED_ORIGINS` - CORS allowed origins (comma-separated)
- `OLLAMA_HOST` - Ollama server URL (optional)

## License

See LICENSE in the root directory.
