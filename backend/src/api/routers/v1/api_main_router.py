from fastapi import APIRouter

from api.models.generic_model import HealthCheckResponse, RootResponse
from api.services.core_service import core_service
from api.routers.v1.chats.api_chat_router import api_chat_router


api_v1_router = APIRouter(
    prefix='/v1',
    tags=['v1'],
)

api_v1_router.include_router(router=api_chat_router)


@api_v1_router.get('/', response_model=RootResponse)
async def root() -> RootResponse:
    """Root endpoint."""
    return RootResponse(message='Welcome to Byte in Bottle API v1')


@api_v1_router.get('/health', response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check v1 endpoint."""
    try:
        available_models = core_service.get_ollama_models()
        return HealthCheckResponse(
            status='healthy',
            ollama='connected',
            available_models=available_models
        )

    except Exception as e:
        return HealthCheckResponse(
            status='degraded', ollama='disconnected', error=str(e)
        )
