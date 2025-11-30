from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models.subscriber_model import Subscriber
from app.schemas.subscriber_schema import SubscriberCreate, SubscriberUpdate


class CRUDSubscriber(CRUDBase[Subscriber, SubscriberCreate, SubscriberUpdate]):

    async def get_by_id(
        self, *, id: UUID, db_session: AsyncSession | None = None
    ) -> Optional[Subscriber]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(select(Subscriber).where(Subscriber.id == id))
        return result.scalar_one_or_none()

    async def get_by_email(
        self, *, email: str, db_session: AsyncSession | None = None
    ) -> Optional[Subscriber]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(
            select(Subscriber).where(Subscriber.email == email)
        )
        return result.scalar_one_or_none()

    async def get_all(self, db_session: AsyncSession | None = None) -> List[Subscriber]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(select(Subscriber))
        return result.scalars().all()


subscriber = CRUDSubscriber(Subscriber)
