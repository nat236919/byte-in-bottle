#!/bin/bash

# Byte in Bottle - Backend Server Startup Script

echo "🍾 Starting Byte in Bottle Backend..."
echo "Powered by bytes. Driven by attitude."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your configuration."
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Default values
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

echo "🚀 Starting server on http://${HOST}:${PORT}"
echo "📝 API docs available at http://localhost:${PORT}/docs"
echo ""

# Start the server
uv run python -m uvicorn backend.main:app --reload --host ${HOST} --port ${PORT}
