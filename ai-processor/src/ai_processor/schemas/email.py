from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class EmailStatus(StrEnum):
    PENDING = "pending"
    FAILED = "failed"
    DONE = "done"


class EmailCategory(StrEnum):
    PRODUCTIVE = "productive"
    UNPRODUCTIVE = "unproductive"


class EmailModel(BaseModel):
    id: str | None = Field(default=None, serialization_alias="_id", validation_alias="_id")
    status: EmailStatus

    title: str
    raw_content: str

    category: EmailCategory | None = None
    quick_answer: str | None = None

    created_at: datetime
    updated_at: datetime
