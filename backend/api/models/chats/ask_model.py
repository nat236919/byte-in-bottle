from typing import Literal
from enum import StrEnum

from pydantic import BaseModel, Field


class AskMode(StrEnum):
    CONCISE = 'concise'
    PROFESSIONAL = 'professional'
    SARCASTIC = 'sarcastic'
    CREATIVE = 'creative'
    FRIENDLY = 'friendly'


class AskRequest(BaseModel):
    model: str = 'llama3.2'
    prompt: str = 'hello world'
    mode: Literal[
        AskMode.CONCISE, AskMode.PROFESSIONAL, AskMode.SARCASTIC,
        AskMode.CREATIVE, AskMode.FRIENDLY
    ] = Field(
        default=AskMode.CONCISE,
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
