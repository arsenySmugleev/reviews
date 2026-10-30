from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.domain.errors import InvalidReviewError

MIN_RATING = 1
MAX_RATING = 5


@dataclass(frozen=True)
class AuthorName:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise InvalidReviewError("author_name must not be empty")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True)
class ReviewText:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise InvalidReviewError("text must not be empty")
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True)
class Rating:
    value: int

    def __post_init__(self) -> None:
        if self.value < MIN_RATING or self.value > MAX_RATING:
            raise InvalidReviewError(
                f"rating must be between {MIN_RATING} and {MAX_RATING}",
            )


@dataclass(frozen=True)
class Review:
    id: UUID
    doctor_id: UUID
    author_name: AuthorName
    rating: Rating
    text: ReviewText
    created_at: datetime

    @classmethod
    def create(
        cls,
        *,
        doctor_id: UUID,
        author_name: str,
        rating: int,
        text: str,
        review_id: UUID | None = None,
        created_at: datetime | None = None,
    ) -> "Review":
        return cls(
            id=review_id or uuid4(),
            doctor_id=doctor_id,
            author_name=AuthorName(author_name),
            rating=Rating(rating),
            text=ReviewText(text),
            created_at=created_at or datetime.now(timezone.utc),
        )
