from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models.topic_model import Topic
from app.schemas.topic_schema import TopicCreate, TopicUpdate


class CRUDTopic(CRUDBase[Topic, TopicCreate, TopicUpdate]):

    async def get_by_id(
        self, *, id: UUID, db_session: AsyncSession | None = None
    ) -> Optional[Topic]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(select(Topic).where(Topic.id == id))
        return result.scalar_one_or_none()

    async def get_by_name(
        self, *, name: str, db_session: AsyncSession | None = None
    ) -> Optional[Topic]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(select(Topic).where(Topic.name == name))
        return result.scalar_one_or_none()

    async def get_all(self, db_session: AsyncSession | None = None) -> List[Topic]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(select(Topic))
        return result.scalars().all()


topic = CRUDTopic(Topic)
