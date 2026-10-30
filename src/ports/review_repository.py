from typing import Protocol
from uuid import UUID

from src.domain import Review


class ReviewRepository(Protocol):
    async def add(self, review: Review) -> Review:
        """Persist a new review and return it."""

    async def list_by_doctor(self, doctor_id: UUID) -> list[Review]:
        """Return all reviews for the given doctor, newest first."""
