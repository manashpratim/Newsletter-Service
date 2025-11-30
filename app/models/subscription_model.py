from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy_utils import ChoiceType
from sqlmodel import Column, Field, Relationship, SQLModel, String

from app.models.base_uuid_model import BaseUUIDModel


class SubscriptionBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Subscription(BaseUUIDModel, SubscriptionBase, table=True):
    subscriber_id: UUID = Field(foreign_key="Subscriber.id")
    topic_id: UUID = Field(foreign_key="Topic.id")

    subscriber: Optional["Subscriber"] = Relationship(back_populates="subscriptions")
    topic: Optional["Topic"] = Relationship(back_populates="subscriptions")
