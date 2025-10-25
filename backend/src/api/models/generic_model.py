from typing import Optional

from pydantic import BaseModel


class RootResponse(BaseModel):
    message: str


class HealthCheckResponse(BaseModel):
    status: str
    ollama: str
    available_models: Optional[list] = []
    error: Optional[str] = None
