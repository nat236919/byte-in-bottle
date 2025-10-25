from api.main import app

__all__ = ["app"]


def main() -> None:
    """Entry point for the application."""
    import uvicorn
    import os
    from dotenv import load_dotenv

    load_dotenv()

    uvicorn.run(
        "api.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )
