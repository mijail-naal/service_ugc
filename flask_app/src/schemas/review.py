from pydantic import BaseModel


class ReviewData(BaseModel):
    user_id: str
    film_id: str
    created_at: str
    user_review: str


class ReviewCondition(BaseModel):
    user_id: str
    film_id: str


class ReviewUpdate(BaseModel):
    user_review: str
