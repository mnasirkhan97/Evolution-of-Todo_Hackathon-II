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
    
    # Phase V: Advanced Fields
    is_recurring: bool = Field(default=False)
    recurrence_interval: Optional[str] = None # daily, weekly, monthly
    due_date: Optional[datetime] = None
    next_occurrence: Optional[datetime] = None

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    is_recurring: Optional[bool] = False
    recurrence_interval: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_recurring: Optional[bool] = None
    recurrence_interval: Optional[str] = None
    due_date: Optional[datetime] = None

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entity_type: str # 'Task', 'User'
    entity_id: str
    action: str # 'CREATE', 'UPDATE', 'DELETE'
    user_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: Optional[str] = None # JSON string

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)
    role: str # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

