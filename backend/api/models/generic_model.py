from typing import Optional
from enum import StrEnum

from pydantic import BaseModel


class RootResponse(BaseModel):
    message: str


class OllamaHealthCheckStatus(StrEnum):
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'


class RedditHealthCheckStatus(StrEnum):
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'


class HealthCheckStatus(StrEnum):
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'
    DEGRADED = 'degraded'


class HealthCheckResponse(BaseModel):
    status: str
    ollama: str
    redis: str
    available_models: Optional[list] = []
    error: Optional[str] = None
