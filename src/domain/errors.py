class DomainError(Exception):
    """Base domain error."""


class InvalidReviewError(DomainError):
    """Rating or text rules violated."""
