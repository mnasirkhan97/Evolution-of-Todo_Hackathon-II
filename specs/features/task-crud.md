# Feature: Task CRUD Operations

## User Stories
- As a user, I can **create** a new task so I can track my work.
- As a user, I can **view** a list of my tasks so I know what to do.
- As a user, I can **update** a task's details if they change.
- As a user, I can **delete** a task I no longer need to do.
- As a user, I can **mark a task as complete** to track progress.

## Acceptance Criteria

### Create Task
- **Input**: Title (Required, 1-200 chars), Description (Optional).
- **Process**: POST `/api/tasks` with JWT.
- **Output**: Returns created task obect.
- **Validation**: Title persistence.

### View Tasks
- **Input**: User navigates to dashboard.
- **Process**: GET `/api/tasks` with JWT.
- **Filter**: Only returns tasks where `task.user_id == current_user.id`.

### Update Task
- **Input**: Edit Title, Description, or Status.
- **Process**: PUT/PATCH `/api/tasks/{id}`.
- **Validation**: Ensure task belongs to user.

### Delete Task
- **Input**: Click delete button.
- **Process**: DELETE `/api/tasks/{id}`.
- **Validation**: Ensure task belongs to user.
