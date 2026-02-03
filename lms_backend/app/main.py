"""FastAPI entrypoint for the LMS backend service.

Run (typical):
    uvicorn app.main:app --host 0.0.0.0 --port 3001

Exposes:
- Health: GET /health, /ready, /live
- Auth: /api/auth/register, /api/auth/login, /api/auth/logout, /api/auth/me
- Courses: /api/courses
- Lessons: /api/lessons/{lesson_id}
- Enrollments: /api/enrollments, /api/enrollments/me
- Progress: /api/progress/me, /api/progress
- Assessments: /api/assessments/{lesson_id}, /api/assessments/{lesson_id}/submit
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.session import engine

# Import models so metadata is populated
from app.db import models  # noqa: F401
from app.db.models.base import Base

openapi_tags = [
    {"name": "Health", "description": "Service health probes."},
    {"name": "Auth", "description": "Authentication and user profile endpoints."},
    {"name": "Courses", "description": "Course catalog endpoints."},
    {"name": "Lessons", "description": "Lesson content endpoints."},
    {"name": "Enrollments", "description": "Enrollments for the authenticated user."},
    {"name": "Progress", "description": "Lesson progress tracking for the authenticated user."},
    {"name": "Assessments", "description": "Lesson assessment endpoints (placeholder implementation)."},
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create database tables on startup (simple scaffold).

    Note: For production, prefer migrations (Alembic). For this scaffold, we auto-create tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Kavia Certified Engineer Learning Platform (LMS).",
    version=settings.app_version,
    openapi_tags=openapi_tags,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS (explicitly allow frontend origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", summary="Root", description="Simple root endpoint to confirm service is running.", tags=["Health"])
async def root() -> dict:
    """Root endpoint."""
    return {"service": "lms_backend", "status": "ok"}
