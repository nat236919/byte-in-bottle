.PHONY: help install run dev test clean

help:
	@echo "🍾 Byte in Bottle - Backend"
	@echo "Powered by bytes. Driven by attitude."
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies with uv"
	@echo "  make run        - Run the server"
	@echo "  make dev        - Run the server with auto-reload"
	@echo "  make test       - Run the API test script"
	@echo "  make clean      - Clean up cache and temp files"

install:
	@echo "📦 Installing dependencies..."
	uv sync

run:
	@echo "🚀 Starting Byte in Bottle Backend..."
	./run.sh

dev:
	@echo "🔧 Starting development server..."
	uv run python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

test:
	@echo "🧪 Testing API..."
	uv run python examples/test_api.py

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✨ Clean!"
