from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


class SubscriberCreate(BaseModel):
    name: Optional[str]
    email: EmailStr


class SubscriberUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr] = None


class SubscriberRead(BaseModel):
    id: UUID
    name: Optional[str]
    email: EmailStr
    created_at: Optional[datetime]
