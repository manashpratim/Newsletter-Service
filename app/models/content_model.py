from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy_utils import ChoiceType
from sqlmodel import (BigInteger, Column, DateTime, Field, Float, Relationship,
                      SQLModel, String)

from app.models.base_uuid_model import BaseUUIDModel


class ContentBase(SQLModel):
    subject: str
    body: str
    scheduled_time: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )


class Content(BaseUUIDModel, ContentBase, table=True):
    topic_id: UUID = Field(foreign_key="Topic.id")
    sent: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    topic: Optional["Topic"] = Relationship(back_populates="contents")
    deliveries: List["DeliveryLog"] = Relationship(back_populates="content")
