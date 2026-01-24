# Backend Guidelines

## Stack
- FastAPI
- SQLModel (ORM)
- Neon PostgreSQL
- Better Auth (JWT Verification)

## Project Structure
- `main.py` - FastAPI app entry point.
- `models.py` - SQLModel database models.
- `routes/` - API route handlers.
- `db.py` - Database connection.

## API Conventions
- All routes under `/api/`.
- Return JSON responses.
- Use Pydantic models for request/response.
- Handle errors with HTTPException.
