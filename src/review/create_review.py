from dataclasses import dataclass
from uuid import UUID

from src.review.domain import Review
from src.review.ports import ReviewRepository


@dataclass(frozen=True)
class CreateReviewInput:
    doctor_id: UUID
    author_name: str
    rating: int
    text: str
    idempotency_key: UUID


class CreateReview:
    def __init__(self, reviews: ReviewRepository) -> None:
        self._reviews = reviews

    async def execute(self, data: CreateReviewInput) -> Review:
        existing = await self._reviews.get_by_idempotency_key(data.idempotency_key)
        if existing is not None:
            return existing

        review = Review.create(
            doctor_id=data.doctor_id,
            author_name=data.author_name,
            rating=data.rating,
            text=data.text,
            idempotency_key=data.idempotency_key,
        )
        return await self._reviews.add(review)
