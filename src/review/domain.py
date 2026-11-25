from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

MIN_RATING = 1
MAX_RATING = 5


class Review(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    doctor_id: UUID
    author_name: str = Field(min_length=1, max_length=200)
    rating: int = Field(ge=MIN_RATING, le=MAX_RATING)
    text: str = Field(min_length=1)
    created_at: datetime
    idempotency_key: UUID

    @classmethod
    def create(
        cls,
        *,
        doctor_id: UUID,
        author_name: str,
        rating: int,
        text: str,
        idempotency_key: UUID,
        review_id: UUID | None = None,
        created_at: datetime | None = None,
    ) -> "Review":
        return cls(
            id=review_id or uuid4(),
            doctor_id=doctor_id,
            author_name=author_name.strip(),
            rating=rating,
            text=text.strip(),
            created_at=created_at or datetime.now(timezone.utc),
            idempotency_key=idempotency_key,
        )
