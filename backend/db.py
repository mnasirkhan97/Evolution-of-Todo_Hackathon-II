from sqlmodel import create_engine, SQLModel, Session
import os
from typing import Generator

# Default to sqlite for local dev if not set, or fail? 
# Spec says Neon Serverless, implies Postgres.
# We'll use a placeholder or expect env var.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./backend_dev.db")

# Basic engine
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    from models import Task, Conversation, Message
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
