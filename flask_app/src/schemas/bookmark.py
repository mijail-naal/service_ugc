from pydantic import BaseModel


class BookmarkData(BaseModel):
    user_id: str
    url: str


class BookmarkCondition(BaseModel):
    user_id: str


class LikeUpdate(BaseModel):
    like: bool
