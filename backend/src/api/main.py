"""
FastAPI application with Ollama integration for byte-in-bottle.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
from typing import Optional, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Ollama client
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
if OLLAMA_HOST:
    ollama_client = ollama.Client(host=OLLAMA_HOST)
else:
    ollama_client = ollama.Client()

app = FastAPI(
    title="Byte in Bottle API",
    description="Powered by bytes. Driven by attitude.",
    version="0.1.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class ChatRequest(BaseModel):
    model: str = "llama3.2"
    messages: List[dict]
    stream: bool = False


class ChatResponse(BaseModel):
    message: dict
    model: str
    created_at: str
    done: bool


class ModelInfo(BaseModel):
    name: str
    size: Optional[int] = None
    digest: Optional[str] = None
    modified_at: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Byte in Bottle API",
        "tagline": "Powered by bytes. Driven by attitude.",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Try to connect to Ollama
        ollama_client.list()
        return {"status": "healthy", "ollama": "connected"}
    except Exception as e:
        return {
            "status": "degraded",
            "ollama": "disconnected",
            "error": str(e)
        }


@app.post("/generate")
async def generate(model: str = "llama3.2", prompt: str = "Hello!"):
    """
    Generate text using an Ollama model.

    Simple endpoint for text generation without chat context.
    """
    try:
        response = ollama_client.generate(model=model, prompt=prompt)
        return {
            "model": model,
            "response": response.get("response", ""),
            "created_at": response.get("created_at", ""),
            "done": response.get("done", True),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )
