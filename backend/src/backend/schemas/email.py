from enum import StrEnum
from datetime import UTC, datetime

from pydantic import BaseModel, Field


class EmailStatus(StrEnum):
    PENDING = "pending"
    FAILED = "failed"
    DONE = "done"


class EmailCategory(StrEnum):
    PRODUCTIVE = "productive"
    UNPRODUCTIVE = "unproductive"


class EmailIn(BaseModel):
    title: str
    content: str


class EmailModel(BaseModel):
    id: str | None = Field(default=None, serialization_alias="_id")
    status: EmailStatus

    title: str
    raw_content: str

    category: EmailCategory | None
    quick_answer: str | None

    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_email_in(email: EmailIn) -> "EmailModel":
        created_at = datetime.now(UTC)
        return EmailModel(
            status=EmailStatus.PENDING,
            title=email.title,
            raw_content=email.content,
            category=None,
            quick_answer=None,
            created_at=created_at,
            updated_at=created_at,
        )


class EmailList(BaseModel):
    page: int
