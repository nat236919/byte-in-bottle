from typing import Literal
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    model: str = 'llama3.2'
    prompt: str = 'hello world'
    mode: Literal[
        'concise', 'professional', 'sarcastic', 'creative', 'friendly'
    ] = Field(
        default='concise',
        description=(
            'Response mode: concise (brief), professional (formal), '
            'sarcastic (witty), creative (imaginative), friendly (casual)'
        )
    )


class AskResponse(BaseModel):
    model: str
    response: str
    created_at: str
    done: bool
    mode: str
