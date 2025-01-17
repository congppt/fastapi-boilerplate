from pydantic import BaseModel


class APICollection(BaseModel):
    chatbot_hook: str
