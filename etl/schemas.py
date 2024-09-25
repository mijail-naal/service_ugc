from pydantic import BaseModel


class DictData(BaseModel):
    topic: str
    offset: int
    key: str
    value: str
    timestamp: int
