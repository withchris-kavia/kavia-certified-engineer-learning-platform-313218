"""Application API router registration."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.assessments import router as assessments_router
from app.api.routes.auth import router as auth_router
from app.api.routes.courses import router as courses_router
from app.api.routes.enrollments import router as enrollments_router
from app.api.routes.health import router as health_router
from app.api.routes.lessons import router as lessons_router
from app.api.routes.progress import router as progress_router

api_router = APIRouter()

# Health endpoints at root level per requirement
api_router.include_router(health_router)

# Core API
api_router.include_router(auth_router)
api_router.include_router(courses_router)
api_router.include_router(lessons_router)
api_router.include_router(enrollments_router)
api_router.include_router(progress_router)
api_router.include_router(assessments_router)
