from fastapi import FastAPI, Body
from dapr.ext.fastapi import DaprApp
from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Optional
from datetime import datetime, timezone
import os
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DB Setup (Duplicate from backend/models.py for independence)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend_dev.db") # Default to dev
engine = create_engine(DATABASE_URL)

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entity_type: str
    entity_id: str
    action: str
    user_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: Optional[str] = None

app = FastAPI()
dapr_app = DaprApp(app)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@dapr_app.subscribe(pubsub='kafka-pubsub', topic='task-events')
def audit_subscriber(event = Body()):
    logger.info(f"Audit log received: {event}")
    
    # Extract data from CloudEvent or raw
    data = event.get("data", {})
    
    try:
        with Session(engine) as session:
            audit = AuditLog(
                entity_type="Task",
                entity_id=str(data.get("task_id", "unknown")),
                action=data.get("event_type", "UNKNOWN").upper(),
                user_id=data.get("user_id", "system"),
                timestamp=datetime.fromisoformat(data.get("timestamp")) if data.get("timestamp") else datetime.now(timezone.utc),
                details=json.dumps(data.get("data", {}))
            )
            session.add(audit)
            session.commit()
            logger.info(f"Audit log saved: {audit.id}")
    except Exception as e:
        logger.error(f"Failed to save audit log: {e}")

    return {"status": "SUCCESS"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6001)
