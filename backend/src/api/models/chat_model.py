from pydantic import BaseModel


class GenerateRequest(BaseModel):
    model: str = 'llama3.2'
    prompt: str = 'hello world'


class GenerateResponse(BaseModel):
    model: str
    response: str
    created_at: str
    done: bool
