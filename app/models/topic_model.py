from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy_utils import ChoiceType
from sqlmodel import (BigInteger, Column, DateTime, Field, Float, Relationship,
                      SQLModel, String)

from app.models.base_uuid_model import BaseUUIDModel


class TopicBase(SQLModel):
    name: str = Field(sa_column=Column(String, index=True, unique=True))
    description: Optional[str] = None


class Topic(BaseUUIDModel, TopicBase, table=True):
    contents: List["Content"] = Relationship(back_populates="topic")
    subscriptions: List["Subscription"] = Relationship(back_populates="topic")
