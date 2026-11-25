from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.review.create_review import CreateReview
from src.review.db import SqlAlchemyReviewRepository, get_session
from src.review.list_reviews import ListReviewsByDoctor


def get_create_review(
    session: AsyncSession = Depends(get_session),
) -> CreateReview:
    return CreateReview(SqlAlchemyReviewRepository(session))


def get_list_reviews_by_doctor(
    session: AsyncSession = Depends(get_session),
) -> ListReviewsByDoctor:
    return ListReviewsByDoctor(SqlAlchemyReviewRepository(session))
