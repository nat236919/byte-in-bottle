from pydantic import BaseModel


class GenerateRequest(BaseModel):
    model: str = 'llama3.2'
    prompt: str


class GenerateResponse(BaseModel):
    model: str
    response: str
    created_at: str
    done: bool
