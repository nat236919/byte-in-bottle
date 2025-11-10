from fastapi import APIRouter

from api.models.generic_model import (
    RootResponse,
    HealthCheckResponse,
    OllamaHealthCheckStatus,
    RedditHealthCheckStatus,
    HealthCheckStatus,
)
from api.services.core_service import core_service
from api.services.cache_service import cache_service
from api.routers.v1.chats.api_chat_router import api_chat_router


api_v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)

api_v1_router.include_router(router=api_chat_router)


@api_v1_router.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    """Root endpoint.

    Returns:
        RootResponse: Welcome message.
    """
    return RootResponse(message="Welcome to Byte in Bottle API v1")


@api_v1_router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check v1 endpoint.

    Returns:
        HealthCheckResponse: Status of Ollama and Redis connections.
    """
    try:
        # Check Ollama connection
        available_models = await core_service.get_ollama_models()
        ollama_status = OllamaHealthCheckStatus.CONNECTED
    except Exception:
        available_models = []
        ollama_status = OllamaHealthCheckStatus.DISCONNECTED

    # Check Redis connection
    redis_healthy = await cache_service.health_check()
    redis_status = (
        RedditHealthCheckStatus.CONNECTED
        if redis_healthy
        else RedditHealthCheckStatus.DISCONNECTED
    )

    # Determine overall status
    overall_status = HealthCheckStatus.UNHEALTHY
    if (
        ollama_status == OllamaHealthCheckStatus.CONNECTED
        and redis_status == RedditHealthCheckStatus.CONNECTED
    ):
        overall_status = HealthCheckStatus.HEALTHY
    elif (
        ollama_status == OllamaHealthCheckStatus.CONNECTED
        or redis_status == RedditHealthCheckStatus.CONNECTED
    ):
        overall_status = HealthCheckStatus.DEGRADED

    return HealthCheckResponse(
        status=overall_status,
        ollama=ollama_status,
        redis=redis_status,
        available_models=available_models,
    )
