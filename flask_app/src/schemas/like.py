from pydantic import BaseModel


class LikeData(BaseModel):
    user_id: str
    film_id: str
    like: bool


class LikeCondition(BaseModel):
    user_id: str
    film_id: str


class LikeUpdate(BaseModel):
    like: bool
