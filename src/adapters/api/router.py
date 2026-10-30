from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.adapters.api.dependencies import get_create_review, get_list_reviews_by_doctor
from src.adapters.api.schemas import ReviewCreate, ReviewResponse
from src.application import CreateReview, CreateReviewInput, ListReviewsByDoctor

router = APIRouter(prefix="/api/v1", tags=["reviews"])


@router.post(
    "/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    body: ReviewCreate,
    use_case: CreateReview = Depends(get_create_review),
) -> ReviewResponse:
    review = await use_case.execute(
        CreateReviewInput(
            doctor_id=body.doctor_id,
            author_name=body.author_name,
            rating=body.rating,
            text=body.text,
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
