from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base_crud import CRUDBase
from app.models.content_model import Content
from app.schemas.content_schema import ContentCreate, ContentUpdate


class CRUDContent(CRUDBase[Content, ContentCreate, ContentUpdate]):

    def _ensure_aware_utc(self, dt: Optional[datetime]) -> Optional[datetime]:
        """
        Convert naive datetimes to UTC-aware datetimes.
        If dt is already tz-aware, convert it to UTC.
        If dt is None, return None.
        """
        if dt is None:
            return None
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    async def get_by_id(
        self, *, id: UUID, db_session: AsyncSession | None = None
    ) -> Optional[Content]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(select(Content).where(Content.id == id))
        return result.scalar_one_or_none()

    async def get_by_topic_id(
        self, *, topic_id: UUID, db_session: AsyncSession | None = None
    ) -> List[Content]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(
            select(Content).where(Content.topic_id == topic_id)
        )
        return result.scalars().all()

    async def get_pending_to_send(
        self, *, as_of: datetime | None = None, db_session: AsyncSession | None = None
    ) -> List[Content]:
        """
        Return contents scheduled to be sent at or before `as_of` and not yet marked sent.
        Default `as_of` is now (UTC).
        """
        db_session = db_session or super().get_db().session
        as_of = as_of or datetime.now(timezone.utc)
        as_of = self._ensure_aware_utc(as_of)
        stmt = select(Content).where(
            and_(Content.sent == False, Content.scheduled_time <= as_of)
        )
        result = await db_session.execute(stmt)
        return result.scalars().all()

    async def get_scheduled_between(
        self, *, start: datetime, end: datetime, db_session: AsyncSession | None = None
    ) -> List[Content]:
        db_session = db_session or super().get_db().session
        start = self._ensure_aware_utc(start)
        end = self._ensure_aware_utc(end)
        stmt = select(Content).where(
            and_(Content.scheduled_time >= start, Content.scheduled_time < end)
        )
        result = await db_session.execute(stmt)
        return result.scalars().all()

    async def mark_sent(
        self, *, id: UUID, db_session: AsyncSession | None = None
    ) -> None:
        db_session = db_session or super().get_db().session
        obj = await self.get_by_id(id=id, db_session=db_session)
        if not obj:
            return
        obj.sent = True
        db_session.add(obj)
        await db_session.commit()
        await db_session.refresh(obj)

    async def get_all(self, db_session: AsyncSession | None = None) -> List[Content]:
        db_session = db_session or super().get_db().session
        result = await db_session.execute(select(Content))
        return result.scalars().all()


content = CRUDContent(Content)
