from uuid import UUID

from src.domain import Review
from src.ports import ReviewRepository


class ListReviewsByDoctor:
    def __init__(self, reviews: ReviewRepository) -> None:
        self._reviews = reviews

    async def execute(self, doctor_id: UUID) -> list[Review]:
        return await self._reviews.list_by_doctor(doctor_id)
