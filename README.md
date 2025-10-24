# byte-in-bottle

Powered by bytes. Driven by attitude.

## Project Structure

- **backend/** - FastAPI + Ollama backend for AI-powered features
- **frontend/** - Frontend application (coming soon)

## Backend

FastAPI application with Ollama integration for local LLM chat and text generation.

### Quick Start (Docker Compose)

The easiest way to run the entire stack:

```bash
# Start both backend and Ollama with llama3.2
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This will:

- Start Ollama service and automatically pull llama3.2 model
- Start the FastAPI backend connected to Ollama
- Backend API available at: <http://localhost:8000>
- API docs at: <http://localhost:8000/docs>

### Quick Start (Local Development)

```bash
cd backend
uv sync
cp .env.example .env
uv run backend
```

See [backend/README.md](backend/README.md) for detailed documentation.

## Features

- 🚀 Fast Python package management with **uv** by Astral
- 🤖 Local LLM integration with **Ollama**
- ⚡ High-performance API with **FastAPI**
- 📝 Auto-generated interactive API documentation

## Prerequisites

### For Docker (Recommended)

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### For Local Development

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.ai/)

## License

See LICENSE file for details.
