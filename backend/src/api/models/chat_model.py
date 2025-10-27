from pydantic import BaseModel


class AskRequest(BaseModel):
    model: str = 'llama3.2'
    prompt: str = 'hello world'


class AskResponse(BaseModel):
    model: str
    response: str
    created_at: str
    done: bool
