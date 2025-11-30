# app/scheduler.py
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from app import crud
from app.db.session import SessionLocal
from app.email import send_newsletter_email

scheduler = AsyncIOScheduler()


async def send_content_job(content_id: str | int):
    async with SessionLocal() as session:
        content = await crud.content.get_by_id(id=content_id, db_session=session)
        print(f"[scheduler] send_content_job - Content: {content}")
        if not content:
            return

        if getattr(content, "sent", False):
            return

        subscribers = await crud.subscription.list_subscribers_for_topic(
            topic_id=content.topic_id, db_session=session
        )

        if not subscribers:
            await crud.content.mark_sent(id=content.id, db_session=session)
            return

        send_any = False
        for sub in subscribers:
            attempt = 0
            last_err = None
            while attempt <= 1:
                try:
                    print(f"[scheduler] sending to {sub.email}: {content.subject}")
                    send_newsletter_email(
                        recipient_email=sub.email,
                        subscriber_name=sub.name,
                        subject=content.subject,
                        body_text=content.body,
                    )
                    err = None
                except Exception as exc:
                    err = str(exc)

                if not err:
                    await crud.delivery_log.create_log(
                        content_id=content.id,
                        subscriber_id=sub.id,
                        status="sent",
                        error=None,
                        db_session=session,
                    )
                    send_any = True
                    break
                else:
                    last_err = err
                    await asyncio.sleep(5)
                    attempt += 1

            if last_err:
                await crud.delivery_log.create_log(
                    content_id=content.id,
                    subscriber_id=sub.id,
                    status="failed",
                    error=last_err,
                    db_session=session,
                )

        if send_any:
            await crud.content.mark_sent(id=content.id, db_session=session)
        else:
            pass


def schedule_content_job(content_id: str | int, run_time: datetime):

    if run_time.tzinfo is None:
        run_time = run_time.replace(tzinfo=timezone.utc)
    else:
        run_time = run_time.astimezone(timezone.utc)

    job_id = f"content_{content_id}"
    trigger = DateTrigger(run_date=run_time)

    scheduler.add_job(
        func=send_content_job,
        trigger=trigger,
        args=[str(content_id)],
        id=job_id,
        replace_existing=True,
    )


async def load_and_schedule_pending():

    print("[scheduler] load_and_schedule_pending running")
    async with SessionLocal() as session:
        all_pending = await crud.content.get_all(db_session=session)
        now = datetime.now(timezone.utc)
        for c in all_pending:
            if getattr(c, "sent", False):
                continue
            run_time = c.scheduled_time
            if not run_time:
                continue

            if run_time.tzinfo is None:
                run_time = run_time.replace(tzinfo=timezone.utc)
            else:
                run_time = run_time.astimezone(timezone.utc)

            if run_time <= now:
                schedule_content_job(c.id, now)
            else:
                schedule_content_job(c.id, run_time)


def start_scheduler():
    if not scheduler.running:
        scheduler.start()

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is not None:
        loop.create_task(load_and_schedule_pending())
    else:

        asyncio.run(load_and_schedule_pending())

    scheduler.add_job(
        load_and_schedule_pending,
        "interval",
        minutes=10,
        id="refresh_pending_contents",
        replace_existing=True,
    )
