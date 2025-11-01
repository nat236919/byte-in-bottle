# Backend

FastAPI backend for Byte in Bottle with LLM integration, caching, and rate limiting.

## Quick Start

**Using Docker Compose (Recommended):**

```bash
docker-compose up --build -d
```

**Local Development:**

```bash
# Install dependencies
brew install redis ollama
brew services start redis
ollama serve

# In a new terminal
ollama pull llama3.2
uv sync
cd src && uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## Configuration

Environment variables (optional):

- `REDIS_URL` - Redis connection (default: `redis://localhost:6379/0`)
- `CACHE_TTL` - Cache TTL in seconds (default: `3600`)
- `RATE_LIMIT_MAX` - Max requests per window (default: `10`)
- `RATE_LIMIT_WINDOW` - Time window in seconds (default: `60`)
- `OLLAMA_HOST` - Ollama API host (default: `http://localhost:11434`)

## API

**Docs:** `http://localhost:8000/docs`

**Endpoints:**

- `GET /v1/health` - Health check
- `POST /v1/chats/ask` - Generate text
