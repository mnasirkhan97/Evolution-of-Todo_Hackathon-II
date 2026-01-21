# Phase I Specification: In-Memory Python Console App

## 1. Overview
This is the first phase of "The Evolution of Todo". The objective is to build a robust, console-based Todo application using Python. The application will store data in-memory (non-persistent across restarts) for this phase.

## 2. Goals
- Demonstrate Spec-Driven Development.
- Implement core CRUD operations.
- Clean, modular Python architecture.

## 3. Functional/User Requirements
The application must provide a CLI loop that accepts commands.

### 3.1. Add Task
- **Command**: `add <title>` or prompt for details.
- **Input**: Title (required), Description (optional).
- **Behavior**: Creates a new task with status `pending`. generated ID.

### 3.2. View Tasks
- **Command**: `list`
- **Behavior**: Displays all tasks in a table or list format.
- **Columns**: ID, Title, Status, Description (truncated).

### 3.3. Update Task
- **Command**: `update <id>`
- **Input**: New Title, New Description. (Blank to keep existing).
- **Behavior**: Updates the specified task.

### 3.4. Mark Complete
- **Command**: `complete <id>`
- **Behavior**: Sets task status to `completed`.

### 3.5. Delete Task
- **Command**: `delete <id>`
- **Behavior**: Removes the task from memory.

### 3.6. Exit
- **Command**: `exit` or `quit`
- **Behavior**: Terminates the application.

## 4. Technical Architecture

### 4.1. Data Model (`src/models.py`)
- **Class `Task`**:
    - `id`: int (auto-incrementing)
    - `title`: str
    - `description`: str (optional)
    - `status`: str (enum: "pending", "completed")
    - `created_at`: datetime

### 4.2. Storage Engine (`src/storage.py`)
- **Class `InMemoryStorage`**:
    - `tasks`: Dict[int, Task]
    - Methods:
        - `add_task(task: Task) -> Task`
        - `get_task(id: int) -> Optional[Task]`
        - `get_all_tasks() -> List[Task]`
        - `update_task(task: Task) -> Task`
        - `delete_task(id: int) -> bool`

### 4.3. CLI Interface (`src/cli.py`)
- **Class `TodoCLI`**:
    - Handling the input loop.
    - Parsing commands.
    - Formatting output (using `rich` library if available, or standard print).

### 4.4. Dependencies
- `uv` (project manager)
- Standard library only, or `rich` for better UI (optional but recommended for "wow" factor). *Decision: Use standard library for Phase 1 simplicity, unless user specified otherwise. User said "Python 3.13+", no external libs mandated, but "Agentic Dev Stack" implies modern tools. Let's stick to standard lib for zero-dependency portability in Phase 1, or minimal deps.* 
- *Refinement*: The Prompt mentions "UV". We should use `pyproject.toml`.
