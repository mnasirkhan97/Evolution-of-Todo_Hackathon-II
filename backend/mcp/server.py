from typing import List, Optional
from mcp.server.fastmcp import FastMCP, Context
from sqlmodel import select, Session
from models import Task, TaskStatus
from db import engine
from datetime import datetime, timezone

# Initialize MCP Server
mcp = FastMCP("todo-mcp-server")

def get_session():
    return Session(engine)

@mcp.tool()
def add_task(user_id: str, title: str, description: Optional[str] = None) -> str:
    """Create a new task for the user."""
    with get_session() as session:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return f"Task created: ID={task.id}, Title='{task.title}'"

@mcp.tool()
def list_tasks(user_id: str, status: Optional[str] = "all") -> str:
    """List tasks for the user. Status can be 'all', 'pending', or 'completed'."""
    with get_session() as session:
        statement = select(Task).where(Task.user_id == user_id)
        if status != "all":
            statement = statement.where(Task.status == status)
        
        tasks = session.exec(statement).all()
        if not tasks:
            return "No tasks found."
            
        result = []
        for t in tasks:
            result.append(f"[{t.id}] {t.title} ({t.status})")
        return "\n".join(result)

@mcp.tool()
def complete_task(user_id: str, task_id: int) -> str:
    """Mark a task as completed."""
    with get_session() as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return f"Task {task_id} not found."
            
        task.status = TaskStatus.COMPLETED
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        return f"Task {task_id} marked as completed."

@mcp.tool()
def delete_task(user_id: str, task_id: int) -> str:
    """Delete a task."""
    with get_session() as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return f"Task {task_id} not found."
            
        session.delete(task)
        session.commit()
        return f"Task {task_id} deleted."

@mcp.tool()
def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> str:
    """Update a task's title or description."""
    with get_session() as session:
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return f"Task {task_id} not found."
            
        if title:
            task.title = title
        if description:
            task.description = description
            
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        return f"Task {task_id} updated."
