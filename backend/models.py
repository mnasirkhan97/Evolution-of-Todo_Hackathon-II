from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True) # Managed by Better Auth
    title: str
    description: Optional[str] = None
    status: str = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
