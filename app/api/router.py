from fastapi import APIRouter

from .endpoints.content import router as content_router
from .endpoints.subscriber import router as subscriber_router
from .endpoints.topic import router as topic_router

api_router = APIRouter()

api_router.include_router(subscriber_router, prefix="/subscriber", tags=["Subscriber"])
api_router.include_router(topic_router, prefix="/topic", tags=["Topic"])
api_router.include_router(content_router, prefix="/content", tags=["Content"])
