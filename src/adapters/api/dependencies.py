from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.db import SqlAlchemyReviewRepository, get_session
from src.application import CreateReview, ListReviewsByDoctor


def get_create_review(
    session: AsyncSession = Depends(get_session),
) -> CreateReview:
    return CreateReview(SqlAlchemyReviewRepository(session))


def get_list_reviews_by_doctor(
    session: AsyncSession = Depends(get_session),
) -> ListReviewsByDoctor:
    return ListReviewsByDoctor(SqlAlchemyReviewRepository(session))
