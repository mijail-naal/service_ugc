from pydantic import BaseModel


class SendMessage(BaseModel):
    topic: str
    key: str
    value: str
