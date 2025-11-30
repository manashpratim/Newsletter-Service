import os
from enum import Enum
from typing import Any

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    PROJECT_NAME: str = os.environ["PROJECT_NAME"]
    DATABASE_USER: str = os.environ["DATABASE_USER"]
    DATABASE_PASSWORD: str = os.environ["DATABASE_PASSWORD"]
    DATABASE_HOST: str = os.environ["DATABASE_HOST"]
    DATABASE_PORT: int = int(os.environ["DATABASE_PORT"])
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]
    DB_POOL_SIZE: int = 83
    WEB_CONCURRENCY: int = 9
    POOL_SIZE: int = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)
    ASYNC_DATABASE_URI: PostgresDsn | str = ""

    @field_validator("ASYNC_DATABASE_URI", mode="after")
    def assemble_db_connection(cls, v: str | None) -> Any:
        if isinstance(v, str):
            if v == "":
                return PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=os.environ["DATABASE_USER"],
                    password=os.environ["DATABASE_PASSWORD"],
                    host=os.environ["DATABASE_HOST"],
                    port=int(os.environ["DATABASE_PORT"]),
                    path=os.environ["DATABASE_NAME"],
                )
        return v

    SECRET_KEY: str = os.environ["SECRET_KEY"]
    ENCRYPT_KEY: str = os.environ["ENCRYPT_KEY"]

    EMAIL_CONNECTION_STRING: str = os.environ["EMAIL_CONNECTION_STRING"]


settings = Settings()
