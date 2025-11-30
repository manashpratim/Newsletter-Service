import os
import sys

absolute_path = os.path.join(os.path.dirname(__file__), "api")

# Add the absolute path to sys.path
sys.path.append(absolute_path)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from sqlalchemy.pool import NullPool, QueuePool
from starlette.middleware.sessions import SessionMiddleware

from app.api.router import api_router as api_router_v1
from app.core.config import settings
from app.utils.exceptions.common_exceptions import CustomException

# Core Application Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=str(settings.ASYNC_DATABASE_URI),
    engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": 100,
        "max_overflow": 100,
        "poolclass": (QueuePool),
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    """
    Global handler for CustomException
    """
    print(f"CustomException occurred: {exc.message}")
    return exc.get_response()


@app.get("/")
async def root():
    """
    An example "Hello world" FastAPI route.
    """
    return {"message": "Hello World"}


@app.on_event("startup")
async def on_startup():
    from app.scheduler import start_scheduler

    start_scheduler()


# Add Routers
app.include_router(api_router_v1, prefix=settings.API_V1_STR)
