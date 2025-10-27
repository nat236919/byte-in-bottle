from fastapi import APIRouter, HTTPException, Request

from api.models.chat_model import GenerateRequest, GenerateResponse
from api.services.core_service import core_service
from api.services.cache_service import cache_service


api_chat_router = APIRouter(
    prefix='/chats',
    tags=['chats'],
    dependencies=[],
)


@api_chat_router.post('/generate', response_model=GenerateResponse)
async def generate(
    request: GenerateRequest, req: Request
) -> GenerateResponse:
    """Generate text using an Ollama model.

    Args:
        request (GenerateRequest): The request body containing model
            and prompt.
        req (Request): FastAPI request object for client info.

    Returns:
        GenerateResponse: The response containing generated text and metadata.

    Raises:
        HTTPException: If generation fails or rate limit exceeded.
    """
    # Get client identifier for rate limiting (IP address)
    client_ip = req.client.host if req.client else 'unknown'

    # Check rate limit
    is_allowed, _ = await cache_service.check_rate_limit(
        client_ip
    )
    if not is_allowed:
        raise HTTPException(
            status_code=429,
            detail=f'Rate limit exceeded. Max {cache_service.rate_limit_max} '
            f'requests per {cache_service.rate_limit_window} seconds',
        )

    # Check cache for existing response
    cached_response = await cache_service.get_cached_response(
        request.model, request.prompt
    )
    if cached_response:
        return GenerateResponse(
            model=request.model,
            response=cached_response.get('response', ''),
            created_at=cached_response.get('created_at', ''),
            done=cached_response.get('done', True),
        )

    # Increment rate limit counter
    await cache_service.increment_rate_limit(client_ip)

    try:
        response = await core_service.generate_text(
            model=request.model, prompt=request.prompt
        )

        # Cache the response for future requests
        response_data = {
            'response': response.get('response', ''),
            'created_at': response.get('created_at', ''),
            'done': response.get('done', True),
        }
        await cache_service.cache_response(
            request.model, request.prompt, response_data
        )

        return GenerateResponse(
            model=request.model,
            response=response.get('response', ''),
            created_at=response.get('created_at', ''),
            done=response.get('done', True),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Generation failed: {str(e)}'
        )
