# System Architecture - Phase II

## High-Level Overview
```mermaid
graph TD
    User((User)) -->|HTTPS| Frontend[Next.js Frontend]
    Frontend -->|API Requests (JWT)| Backend[FastAPI Backend]
    Frontend -->|Auth Requests| Auth[Better Auth]
    Backend -->|SQL| DB[(Neon PostgreSQL)]
    Auth -->|Session/Tokens| DB
```

## detailed Components

### Frontend (Next.js)
- **Pages**: `/dashboard`, `/login`, `/signup`.
- **Client**: `lib/api.ts` handles REST calls.
- **State**: Server Components for fetching, React State for forms.

### Backend (FastAPI)
- **Middleware**: Validates JWT from Better Auth.
- **Routes**: `/api/tasks`, `/api/user`.
- **ORM**: SQLModel for DB interaction.

### Database (PostgreSQL)
- **Users Table**: Managed by Better Auth.
- **Tasks Table**: User-specific tasks.
