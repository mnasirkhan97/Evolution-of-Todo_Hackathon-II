# Evolution of Todo - Phase II Setup Guide

## 1. Prerequisites
- **Node.js**: v18+
- **Python**: v3.11+
- **Docker** (Optional, for simplified run)
- **Neon Database**: A free Postgres instance from neon.tech

## 2. Environment Setup

Copy the example environment file:
```bash
cp .env.example .env
```

**Required Updates in `.env`:**
1. **`DATABASE_URL`**: Get this from your Neon Dashboard.
   - Format: `postgresql://<user>:<password>@<host>/<dbname>?sslmode=require`
2. **`BETTER_AUTH_SECRET`**: Generate a random string or use the default for dev.

## 3. Running the Application

### Option A: Docker Compose (Recommended)
This runs both frontend and backend automatically.
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Option B: Manual Mode
**Backend Terminal**:
```bash
cd backend
# Create venv if not exists
python -m venv venv
# Activate (Windows)
.\venv\Scripts\activate
# Install deps
pip install -r requirements.txt
# Run
uvicorn main:app --reload
```

**Frontend Terminal**:
```bash
cd frontend
# Install deps
npm install
# Run
npm run dev
```

## 4. Verification Flow
1. Open http://localhost:3000
2. Click **Sign Up** -> Create account.
3. You should be redirected to the Dashboard.
4. Add a Task -> Ensure it appears.
5. Refresh page -> Ensure task persists (DB check).
