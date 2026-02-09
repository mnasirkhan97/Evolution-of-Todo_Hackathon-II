# Feature: Todo AI Chatbot (Phase III)

## Goal
Create an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture and OpenAI Agents SDK.

## Architecture
- **Frontend**: WebSocket/HTTP Chat Interface (OpenAI ChatKit UI)
- **Backend**: FastAPI Server
    - Chat Endpoint: `POST /api/{user_id}/chat`
    - Logic: OpenAI Agents SDK (Stateless Agent + Runner)
    - Tools: MCP Server (Official MCP SDK) exposing Task CRUD.
- **Database**: Neon Serverless PostgreSQL (SQLModel)
    - Stores: `Task`, `Conversation`, `Message`.
- **Auth**: Better Auth (User ID propagation).

## Technical Requirements

### Database Models
- **Task**: `user_id`, `id`, `title`, `description`, `completed`, `created_at`, `updated_at`
- **Conversation**: `user_id`, `id`, `created_at`, `updated_at`
- **Message**: `user_id`, `id`, `conversation_id`, `role` (user/assistant), `content`, `created_at`

### API Endpoints
#### `POST /api/{user_id}/chat`
- **Input**:
    - `conversation_id` (optional, integer)
    - `message` (required, string)
- **Processing**:
    1. Fetch conversation history from DB.
    2. Store user message in DB.
    3. Run Agent (OpenAI Agents SDK) with MCP tools.
    4. Store assistant response in DB.
- **Output**:
    - `conversation_id`: integer
    - `response`: string
    - `tool_calls`: array (debug info)

### MCP Tools Specification
The MCP server must expose the following tools:
1. **`add_task(user_id, title, description)`**: Create a new task.
2. **`list_tasks(user_id, status)`**: Retrieve tasks (status: "all", "pending", "completed").
3. **`complete_task(user_id, task_id)`**: Mark task as complete.
4. **`delete_task(user_id, task_id)`**: Remove a task.
5. **`update_task(user_id, task_id, title, description)`**: Modify task.

### Agent Behavior
- **Stateless**: Server holds NO state between requests.
- **Context**: Rebuilds context from DB history for every request.
- **Natural Language**: Handles commands like "Add a task...", "What's pending?", "Delete the meeting task".

## Frontend (ChatKit)
- **UI**: ChatKit-based UI.
- **Config**: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` needed for hosted components (if applicable).
