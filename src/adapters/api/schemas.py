from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.domain import MAX_RATING, MIN_RATING


class ReviewCreate(BaseModel):
    doctor_id: UUID
    author_name: str = Field(min_length=1, max_length=30)
    rating: int = Field(ge=MIN_RATING, le=MAX_RATING)
    text: str = Field(min_length=1)


class ReviewResponse(BaseModel):
    id: UUID
    doctor_id: UUID
    author_name: str
    rating: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, review) -> "ReviewResponse":
        return cls(
            id=review.id,
            doctor_id=review.doctor_id,
            author_name=review.author_name.value,
            rating=review.rating.value,
            text=review.text.value,
            created_at=review.created_at,
        )
