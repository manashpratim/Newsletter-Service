from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models.subscriber_model import Subscriber
from app.models.subscription_model import Subscription
from app.schemas.subscription_schema import (SubscriptionCreate,
                                             SubscriptionUpdate)


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):

    async def get_by_id(
        self, *, id: UUID, db_session: AsyncSession | None = None
    ) -> Optional[Subscription]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(
            select(Subscription).where(Subscription.id == id)
        )
        return result.scalar_one_or_none()

    async def get_for_subscriber(
        self, *, subscriber_id: UUID, db_session: AsyncSession | None = None
    ) -> List[Subscription]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(
            select(Subscription).where(Subscription.subscriber_id == subscriber_id)
        )
        return result.scalars().all()

    async def get_for_topic(
        self, *, topic_id: UUID, db_session: AsyncSession | None = None
    ) -> List[Subscription]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(
            select(Subscription).where(Subscription.topic_id == topic_id)
        )
        return result.scalars().all()

    async def list_subscribers_for_topic(
        self, *, topic_id: UUID, db_session: AsyncSession | None = None
    ) -> List[Subscriber]:

        db_session = db_session or super().get_db().session
        stmt = (
            select(Subscriber)
            .join(Subscription, Subscription.subscriber_id == Subscriber.id)
            .where(Subscription.topic_id == topic_id)
        )
        result = await db_session.execute(stmt)
        return result.scalars().all()


subscription = CRUDSubscription(Subscription)
