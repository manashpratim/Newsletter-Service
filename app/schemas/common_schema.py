from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"
