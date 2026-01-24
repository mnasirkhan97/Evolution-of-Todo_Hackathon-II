# Database Schema

## Tables

### `user` (Managed by Better Auth)
*Note: Better Auth manages this, but we reference `id`.*
- `id`: string (Primary Key)
- `email`: string (Unique)
- `name`: string
- `created_at`: datetime

### `task`
- `id`: int (Primary Key, Auto-increment)
- `user_id`: string (Foreign Key -> user.id, Index)
- `title`: string (Not Null)
- `description`: text (Nullable)
- `status`: string (Enum: "pending", "completed", default: "pending")
- `created_at`: datetime (default: now)
- `updated_at`: datetime (default: now)

## Relationships
- One User has Many Tasks.
- Tasks are strictly isolated by `user_id`.
