# REST API Endpoints

## Base URL
- Local: `http://localhost:8000`

## Authentication
- **Header**: `Authorization: Bearer <token>`
- **Response if missing/invalid**: `401 Unauthorized`

## Endpoints

### Tasks

#### `GET /api/tasks`
- **Desc**: Get all tasks for the authenticated user.
- **Response**: `List[Task]`

#### `POST /api/tasks`
- **Desc**: Create a new task.
- **Body**: `{"title": "string", "description": "string"}`
- **Response**: `Task`

#### `GET /api/tasks/{id}`
- **Desc**: Get a specific task.
- **Response**: `Task` or `404`

#### `PUT /api/tasks/{id}`
- **Desc**: Update a task.
- **Body**: `{"title": "string", "description": "string", "status": "string"}`
- **Response**: `Task`

#### `DELETE /api/tasks/{id}`
- **Desc**: Delete a task.
- **Response**: `{"ok": true}`
