from fastapi import APIRouter

from api.models.generic_model import HealthCheckResponse, RootResponse
from api.services.core_service import core_service
from api.services.cache_service import cache_service
from api.routers.v1.chats.api_chat_router import api_chat_router


api_v1_router = APIRouter(
    prefix='/v1',
    tags=['v1'],
)

api_v1_router.include_router(router=api_chat_router)


@api_v1_router.get('/', response_model=RootResponse)
async def root() -> RootResponse:
    """Root endpoint.

    Returns:
        RootResponse: Welcome message.
    """
    return RootResponse(message='Welcome to Byte in Bottle API v1')


@api_v1_router.get('/health', response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check v1 endpoint.

    Returns:
        HealthCheckResponse: Status of Ollama and Redis connections.
    """
    try:
        # Check Ollama connection
        available_models = await core_service.get_ollama_models()
        ollama_status = 'connected'
    except Exception:
        available_models = []
        ollama_status = 'disconnected'

    # Check Redis connection
    redis_healthy = await cache_service.health_check()
    redis_status = 'connected' if redis_healthy else 'disconnected'

    # Determine overall status
    overall_status = 'unhealthy'
    if ollama_status == 'connected' and redis_status == 'connected':
        overall_status = 'healthy'
    elif ollama_status == 'connected' or redis_status == 'connected':
        overall_status = 'degraded'

    return HealthCheckResponse(
        status=overall_status,
        ollama=ollama_status,
        redis=redis_status,
        available_models=available_models,
    )
