from typing import Protocol
from uuid import UUID

from src.review.domain import Review


class ReviewRepository(Protocol):
    async def add(self, review: Review) -> Review:
        ...

    async def list_by_doctor(self, doctor_id: UUID) -> list[Review]:
        ...

    async def get_by_idempotency_key(self, key: UUID) -> Review | None:
        ...
