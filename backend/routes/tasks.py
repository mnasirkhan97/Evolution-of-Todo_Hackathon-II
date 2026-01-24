from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone

from db import get_session
from models import Task, TaskCreate, TaskUpdate
from auth import get_current_user_id

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

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
    return {"ok": True}
