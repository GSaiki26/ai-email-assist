from enum import StrEnum

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

    @staticmethod
    def from_email_in(email: EmailIn) -> "EmailModel":
        return EmailModel(
            status=EmailStatus.PENDING,
            title=email.title,
            raw_content=email.content,
            category=None,
            quick_answer=None,
        )


class EmailList(BaseModel):
    page: int
