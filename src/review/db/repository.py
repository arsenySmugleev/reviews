from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.review.db.models import ReviewModel
from src.review.domain import Review


class SqlAlchemyReviewRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, review: Review) -> Review:
        row = ReviewModel(
            id=review.id,
            doctor_id=review.doctor_id,
            author_name=review.author_name,
            rating=review.rating,
            text=review.text,
            created_at=review.created_at,
            idempotency_key=review.idempotency_key,
        )
        self._session.add(row)
        try:
            await self._session.flush()
        except IntegrityError:
            await self._session.rollback()
            existing = await self.get_by_idempotency_key(review.idempotency_key)
            if existing is not None:
                return existing
            raise
        return review

    async def list_by_doctor(self, doctor_id: UUID) -> list[Review]:
        result = await self._session.execute(
            select(ReviewModel)
            .where(ReviewModel.doctor_id == doctor_id)
            .order_by(ReviewModel.created_at.desc())
        )
        rows = result.scalars().all()
        return [self._to_domain(row) for row in rows]

    async def get_by_idempotency_key(self, key: UUID) -> Review | None:
        result = await self._session.execute(
            select(ReviewModel).where(ReviewModel.idempotency_key == key)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return self._to_domain(row)

    @staticmethod
    def _to_domain(row: ReviewModel) -> Review:
        return Review(
            id=row.id,
            doctor_id=row.doctor_id,
            author_name=row.author_name,
            rating=row.rating,
            text=row.text,
            created_at=row.created_at,
            idempotency_key=row.idempotency_key,
        )
