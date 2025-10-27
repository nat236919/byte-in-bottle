# Backend

FastAPI backend for Byte in Bottle.

## Features

- **FastAPI** - Modern async web framework
- **Ollama** - LLM integration for text generation
- **Redis** - Caching and rate limiting
- **Async I/O** - Non-blocking operations for better concurrency
- **Multiple Workers** - Parallel request processing

## Quick Start

### Option 1: Using Docker Compose (Recommended)

Run the entire stack including Ollama and Redis:

```bash
# From the project root directory
docker-compose up --build -d
```

This will:

- Start Redis service on port 6379
- Start Ollama service on port 11434
- Pull the llama3.2 model automatically
- Start the FastAPI backend on port 8000 with caching and rate limiting

### Option 2: Local Development

If you want to run the backend locally, you need Ollama and Redis running first:

```bash
# 1. Install and start Redis (if not already running)
# macOS:
brew install redis
brew services start redis

# Or using Docker:
docker run -d -p 6379:6379 redis:7-alpine

# 2. Install and start Ollama (if not already running)
# Download from https://ollama.ai or use brew:
# brew install ollama

# 3. Start Ollama service
ollama serve

# 4. Pull the model (in a new terminal)
ollama pull llama3.2

# 5. Set environment variables (optional, defaults to localhost)
export OLLAMA_HOST=http://localhost:11434
export REDIS_URL=redis://localhost:6379/0

# 6. Install dependencies
uv sync

# 7. Run development server
cd src && uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## Configuration

Configure the backend using environment variables (see `.env.example`):

### Redis Caching

- `REDIS_URL` - Redis connection URL (default: `redis://localhost:6379/0`)
- `CACHE_TTL` - Cache time-to-live in seconds (default: `3600` - 1 hour)

### Rate Limiting

- `RATE_LIMIT_MAX` - Max requests per window (default: `10`)
- `RATE_LIMIT_WINDOW` - Time window in seconds (default: `60`)

### Ollama

- `OLLAMA_HOST` - Ollama API host (default: `http://localhost:11434`)

## Caching & Rate Limiting

The backend implements smart caching and rate limiting:

**Response Caching:**

- LLM responses are cached based on model + prompt hash
- Reduces redundant API calls to Ollama
- Configurable TTL (default: 1 hour)
- Automatic cache invalidation

**Rate Limiting:**

- IP-based request throttling
- Prevents API abuse
- Configurable limits (default: 10 requests/minute)
- Returns HTTP 429 when exceeded

## Stack

- **FastAPI** - Web framework
- **Ollama** - LLM integration
- **Redis** - Caching and rate limiting
- **uvicorn** - ASGI server (4 workers for concurrency)

## API

Swagger docs: `http://localhost:8000/docs`

### Key Endpoints

- `GET /v1/health` - Health check with Ollama and Redis status
- `POST /v1/chats/generate` - Generate text with caching and rate limiting
