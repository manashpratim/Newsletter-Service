from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy_utils import ChoiceType
from sqlmodel import Column, Field, Relationship, SQLModel, String

from app.models.base_uuid_model import BaseUUIDModel


class SubscriberBase(SQLModel):
    name: str
    email: str = Field(sa_column=Column(String, index=True, unique=True))


class Subscriber(BaseUUIDModel, SubscriberBase, table=True):
    subscriptions: List["Subscription"] = Relationship(back_populates="subscriber")
