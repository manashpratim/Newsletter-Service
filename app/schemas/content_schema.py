from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


def _parse_iso_datetime_to_aware(dt_in) -> datetime:

    if dt_in is None:
        raise ValueError("datetime value is required")

    if isinstance(dt_in, datetime):
        if dt_in.tzinfo is None:
            return dt_in.replace(tzinfo=timezone.utc)
        return dt_in.astimezone(timezone.utc)

    if isinstance(dt_in, str):
        s = dt_in.strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(s)
        except Exception as e:
            raise ValueError(f"Invalid datetime format: {dt_in!r}") from e

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    raise ValueError("Unsupported datetime input type")


class ContentCreate(BaseModel):
    topic_id: UUID
    subject: str
    body: str
    scheduled_time: datetime

    @field_validator("subject")
    def subject_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("subject must not be empty")
        return v

    @field_validator("scheduled_time", mode="before")
    def ensure_tz_aware(cls, v) -> datetime:
        try:
            return _parse_iso_datetime_to_aware(v)
        except ValueError as exc:
            raise ValueError(
                [{"loc": ("scheduled_time",), "msg": str(exc), "type": "value_error"}]
            )


class ContentUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    sent: Optional[bool] = None

    @field_validator("subject")
    def strip_subject_if_present(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v

    @field_validator("scheduled_time", mode="before")
    def ensure_tz_aware_optional(cls, v) -> Optional[datetime]:
        if v is None:
            return None
        try:
            return _parse_iso_datetime_to_aware(v)
        except ValueError as exc:
            raise ValueError(
                [{"loc": ("scheduled_time",), "msg": str(exc), "type": "value_error"}]
            )


class ContentRead(BaseModel):
    id: UUID
    topic_id: UUID
    subject: str
    body: str
    scheduled_time: datetime
    sent: bool
    created_at: Optional[datetime]
