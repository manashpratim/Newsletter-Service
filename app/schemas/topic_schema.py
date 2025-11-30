from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


class TopicCreate(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("topic name must not be empty")
        return v


class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    @field_validator("name")
    def maybe_strip_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v


class TopicRead(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: Optional[datetime]
