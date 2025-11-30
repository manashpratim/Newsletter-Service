from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


class SubscriptionCreate(BaseModel):
    subscriber_id: UUID
    topic_id: UUID


class SubscriptionUpdate(SubscriptionCreate):
    pass


class SubscriptionRead(BaseModel):
    id: UUID
    subscriber_id: UUID
    topic_id: UUID
    created_at: Optional[datetime]
