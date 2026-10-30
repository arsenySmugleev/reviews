from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.db.models import ReviewModel
from src.domain import AuthorName, Rating, Review, ReviewText


class SqlAlchemyReviewRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, review: Review) -> Review:
        row = ReviewModel(
            id=review.id,
            doctor_id=review.doctor_id,
            author_name=review.author_name.value,
            rating=review.rating.value,
            text=review.text.value,
            created_at=review.created_at,
        )
        self._session.add(row)
        await self._session.flush()
        return review

    async def list_by_doctor(self, doctor_id: UUID) -> list[Review]:
        result = await self._session.execute(
            select(ReviewModel)
            .where(ReviewModel.doctor_id == doctor_id)
            .order_by(ReviewModel.created_at.desc())
        )
        rows = result.scalars().all()
        return [self._to_domain(row) for row in rows]

    @staticmethod
    def _to_domain(row: ReviewModel) -> Review:
        return Review(
            id=row.id,
            doctor_id=row.doctor_id,
            author_name=AuthorName(row.author_name),
            rating=Rating(row.rating),
            text=ReviewText(row.text),
            created_at=row.created_at,
        )
