from typing import Protocol
from uuid import UUID

from src.domain import Review


class ReviewRepository(Protocol):
    async def add(self, review: Review) -> Review:
        ...

    async def list_by_doctor(self, doctor_id: UUID) -> list[Review]:
        ...
