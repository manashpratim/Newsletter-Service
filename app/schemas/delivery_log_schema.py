from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


class DeliveryStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class DeliveryLogCreate(BaseModel):
    id: UUID
    content_id: UUID
    subscriber_id: UUID
    status: DeliveryStatus = DeliveryStatus.PENDING


class DeliveryLogUpdate(DeliveryLogCreate):
    status: DeliveryStatus
    error: Optional[str]
    sent_at: Optional[datetime]


class DeliveryLogRead(BaseModel):
    id: UUID
    content_id: UUID
    subscriber_id: UUID
    status: DeliveryStatus
    error: Optional[str]
    sent_at: Optional[datetime]
