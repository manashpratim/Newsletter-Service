from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models.delivery_log_model import DeliveryLog
from app.schemas.delivery_log_schema import (DeliveryLogCreate,
                                             DeliveryLogUpdate)


class CRUDDeliveryLog(CRUDBase[DeliveryLog, DeliveryLogCreate, DeliveryLogUpdate]):

    async def get_by_id(
        self, *, id: UUID, db_session: AsyncSession | None = None
    ) -> Optional[DeliveryLog]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(
            select(DeliveryLog).where(DeliveryLog.id == id)
        )
        return result.scalar_one_or_none()

    async def list_for_content(
        self, *, content_id: UUID, db_session: AsyncSession | None = None
    ) -> List[DeliveryLog]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(
            select(DeliveryLog).where(DeliveryLog.content_id == content_id)
        )
        return result.scalars().all()

    async def list_for_subscriber(
        self, *, subscriber_id: UUID, db_session: AsyncSession | None = None
    ) -> List[DeliveryLog]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(
            select(DeliveryLog).where(DeliveryLog.subscriber_id == subscriber_id)
        )
        return result.scalars().all()

    async def create_log(
        self,
        *,
        content_id: UUID,
        subscriber_id: UUID,
        status: str,
        error: Optional[str] = None,
        db_session: AsyncSession | None = None,
    ) -> DeliveryLog:
        db_session = db_session or super().get_db().session
        obj = DeliveryLog(
            content_id=content_id,
            subscriber_id=subscriber_id,
            status=status,
            error=error,
            sent_at=datetime.utcnow(),
        )
        db_session.add(obj)
        await db_session.commit()
        await db_session.refresh(obj)
        return obj


delivery_log = CRUDDeliveryLog(DeliveryLog)
