from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy_utils import ChoiceType
from sqlmodel import (BigInteger, Column, DateTime, Field, Float, Relationship,
                      SQLModel, String)

from app.models.base_uuid_model import BaseUUIDModel


class DeliveryLogBase(SQLModel):
    status: str = "pending"  # "pending", "sent", "failed"
    error: Optional[str] = None
    sent_at: Optional[datetime] = None


class DeliveryLog(BaseUUIDModel, DeliveryLogBase, table=True):
    content_id: UUID = Field(foreign_key="Content.id")
    subscriber_id: UUID = Field(foreign_key="Subscriber.id")

    content: Optional["Content"] = Relationship(back_populates="deliveries")
