# Backend

FastAPI backend for Byte in Bottle.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

Run the entire stack including Ollama:

```bash
# From the project root directory
docker-compose up -d
```

This will:

- Start Ollama service on port 11434
- Pull the llama3.2 model automatically
- Start the FastAPI backend on port 8000

### Option 2: Local Development

If you want to run the backend locally, you need Ollama running first:

```bash
# 1. Install and start Ollama (if not already running)
# Download from https://ollama.ai or use brew:
# brew install ollama

# 2. Start Ollama service
ollama serve

# 3. Pull the model (in a new terminal)
ollama pull llama3.2

# 4. Set environment variable (optional, defaults to localhost)
export OLLAMA_HOST=http://localhost:11434

# 5. Install dependencies
uv sync

# 6. Run development server
cd src && uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## Stack

- **FastAPI** - Web framework
- **Ollama** - LLM integration
- **uvicorn** - ASGI server

## API

Swagger docs: `http://localhost:8000/docs`
