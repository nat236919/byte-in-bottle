from fastapi import APIRouter, HTTPException

from api.models.chat_model import GenerateRequest, GenerateResponse
from api.services.core_service import core_service


api_chat_router = APIRouter(
    prefix='/chats',
    tags=['chats'],
    dependencies=[],
)


@api_chat_router.post('/generate', response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    """Generate text using an Ollama model.

    Args:
        request (GenerateRequest): The request body containing model
            and prompt.

    Returns:
        GenerateResponse: The response containing generated text and metadata.

    Raises:
        HTTPException: If generation fails.
    """
    try:
        response = await core_service.generate_text(
            model=request.model, prompt=request.prompt
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
