# Byte In Bottle

Powered by bytes. Driven by attitude.

## Project Structure

- **backend/** - FastAPI + Ollama backend for AI-powered features
- **frontend/** - Nuxt 4 frontend application

## Backend

FastAPI application with Ollama integration for local LLM chat and text generation.

## Frontend

Modern web application built with:

- **Nuxt 4** - The Intuitive Vue Framework
- **TypeScript** - Type-safe development
- **Chat Interface** - Real-time chat with AI models

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
