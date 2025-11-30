# Newsletter-Service
A production-ready asynchronous newsletter delivery system built using FastAPI, SQLModel, PostgreSQL, and APScheduler.

This service allows you to:

Create and manage subscribers

Create and manage topics

Allow subscribers to subscribe/unsubscribe from topics

Create content items assigned to topics

Schedule content to be sent at specific dates/times

Automatically send newsletters to all subscribers of that topic

Track delivery logs (success/failure)

Trigger send-now for manual email delivery

Use Azure Communication Services or SMTP to send emails

Fully asynchronous & background-task safe

🚀 Features
✅ Subscriber Management

Add subscribers (name + email)

Prevent duplicates

Subscribe/unsubscribe to topics

✅ Topic Management

Create topics

Each subscriber subscribes to 1 or more topics

✅ Content System

Create newsletter content

Assign each content item to a topic

Set a UTC scheduled_time

Mark content as sent

✅ Automated Job Scheduler

APScheduler (AsyncIO) based

Schedules each content item to send at the correct time

Periodic background job refreshes the schedule every 2 minutes

Recovers from DB/network failures (retry + exponential backoff)

send_content_job handles delivery + logging

✅ Email Delivery

Azure Communication Services

Uses EmailClient

Structured HTML templates

Production grade reliability


Automatic HTML + plain-text fallback

✅ REST API

/subscribers/*

/topics/*

/content/*

/content/{id}/send-now — manual trigger

Fully typed Pydantic schemas

Common response wrappers


📦 Installation
1. Clone the repository
git clone https://github.com/<your-username>/newsletter-service.git
cd newsletter-service

2. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Running the App
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Known Limitations

APScheduler jobs are in-memory — not persistent across restarts unless a jobstore is added.

If you run multiple backend replicas, you must choose one active scheduler (or use distributed locking).

Azure Communication Services requires verified domain.


Future Improvements

Add Redis/Celery for distributed job queues

Add persistent APScheduler jobstore (PostgreSQL)

Add bulk email + parallel delivery

Add HTML template editor for newsletters

Add webhook-based bounce/unsubscribe tracking
