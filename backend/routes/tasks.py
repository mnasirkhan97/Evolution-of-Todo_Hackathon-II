from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone
import json

from db import get_session
from models import Task, TaskCreate, TaskUpdate
from auth import get_current_user_id

# Dapr Import
try:
    from dapr.clients import DaprClient
    DAPR_AVAILABLE = True
except ImportError:
    DAPR_AVAILABLE = False
    print("Dapr SDK not installed/available. Skipping events.")

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

PUBSUB_NAME = "kafka-pubsub"
TOPIC_NAME = "task-events"

def publish_task_event(event_type: str, task: Task):
    """Publish task event to Dapr PubSub."""
    if not DAPR_AVAILABLE:
        return

    try:
        with DaprClient() as d:
             # Serialize task manually or use model_dump_json()
             event_data = {
                 "event_type": event_type,
                 "task_id": task.id,
                 "user_id": task.user_id,
                 "timestamp": datetime.now(timezone.utc).isoformat(),
                 "data": json.loads(task.model_dump_json())
             }
             d.publish_event(
                 pubsub_name=PUBSUB_NAME,
                 topic_name=TOPIC_NAME,
                 data=json.dumps(event_data),
                 data_content_type="application/json"
             )
             print(f"Published event: {event_type} for task {task.id}")
    except Exception as e:
        print(f"Failed to publish event: {e}")

@router.get("", response_model=List[Task])
def list_tasks(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
    status: Optional[str] = Query(None, description="Filter by status")
):
    query = select(Task).where(Task.user_id == user_id)
    if status:
        query = query.where(Task.status == status)
    tasks = session.exec(query).all()
    return tasks

@router.post("", response_model=Task)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    db_task = Task.model_validate(task)
    db_task.user_id = user_id
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    # Phase V: Publish Event
    publish_task_event("created", db_task)
    
    return db_task

@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    db_task.updated_at = datetime.now(timezone.utc)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    # Phase V: Publish Event
    publish_task_event("updated", db_task)
    
    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(db_task)
    session.commit()
    
    # Phase V: Publish Event (Must invoke before commit? No, after is safer but object is detached. 
    # Actually, deleted object might not serialize well if lazy loaded.
    # We should serialize before delete or just send ID.
    # Let's send a minimal event for delete or re-construct data.)
    # Ideally we'd do it before delete commit, but let's just send ID and user_id.
    try:
         # Minimal event for deletion
         if DAPR_AVAILABLE:
            with DaprClient() as d:
                event_data = {
                    "event_type": "deleted",
                    "task_id": task_id,
                    "user_id": user_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "data": {} # No data for delete
                }
                d.publish_event(
                    pubsub_name=PUBSUB_NAME,
                    topic_name=TOPIC_NAME,
                    data=json.dumps(event_data),
                    data_content_type="application/json"
                )
    except Exception:
        pass

    return {"ok": True}
