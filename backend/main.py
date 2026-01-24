from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load .env from root (parent of backend)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
from db import init_db
from routes import tasks
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    init_db()
    yield
    # Shutdown

app = FastAPI(title="Evolution of Todo API", lifespan=lifespan)

# CORS Configuration - Allow Frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Evolution of Todo API (Phase II)"}
