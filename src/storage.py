from typing import List, Optional, Dict
from src.models import Task, TaskStatus

class InMemoryStorage:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Creates and stores a new task."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieves a task by ID."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Retrieves all tasks, ordered by ID."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Updates an existing task's title and/or description."""
        task = self.get_task(task_id)
        if not task:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
            
        return task

    def mark_complete(self, task_id: int) -> Optional[Task]:
        """Marks a task as complete."""
        task = self.get_task(task_id)
        if not task:
            return None
        
        task.status = TaskStatus.COMPLETED
        return task

    def delete_task(self, task_id: int) -> bool:
        """Deletes a task by ID. Returns True if deleted, False if not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
