from dataclasses import dataclass
from uuid import UUID

from src.domain import Review
from src.ports import ReviewRepository


@dataclass(frozen=True)
class CreateReviewInput:
    doctor_id: UUID
    author_name: str
    rating: int
    text: str


class CreateReview:
    def __init__(self, reviews: ReviewRepository) -> None:
        self._reviews = reviews

    async def execute(self, data: CreateReviewInput) -> Review:
        review = Review.create(
            doctor_id=data.doctor_id,
            author_name=data.author_name,
            rating=data.rating,
            text=data.text,
        )
        return await self._reviews.add(review)
