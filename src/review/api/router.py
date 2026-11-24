from uuid import UUID

from fastapi import APIRouter, Depends, Header, status

from src.review.api.dependencies import get_create_review, get_list_reviews_by_doctor
from src.review.api.schemas import ReviewCreate, ReviewResponse
from src.review.create_review import CreateReview, CreateReviewInput
from src.review.list_reviews import ListReviewsByDoctor

router = APIRouter(prefix="/api/v1", tags=["reviews"])


@router.post(
    "/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    body: ReviewCreate,
    use_case: CreateReview = Depends(get_create_review),
    idempotency_key: UUID = Header(..., alias="Idempotency-Key"),
) -> ReviewResponse:
    review = await use_case.execute(
        CreateReviewInput(
            doctor_id=body.doctor_id,
            author_name=body.author_name,
            rating=body.rating,
            text=body.text,
            idempotency_key=idempotency_key,
        )
    )
    return ReviewResponse.from_domain(review)


@router.get(
    "/doctors/{doctor_id}/reviews",
    response_model=list[ReviewResponse],
)
async def list_doctor_reviews(
    doctor_id: UUID,
    use_case: ListReviewsByDoctor = Depends(get_list_reviews_by_doctor),
) -> list[ReviewResponse]:
    reviews = await use_case.execute(doctor_id)
    return [ReviewResponse.from_domain(review) for review in reviews]
