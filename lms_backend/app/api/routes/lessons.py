"""Lesson API routes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.lesson import Lesson
from app.db.session import get_db_session
from app.schemas.lessons import LessonOut

router = APIRouter(prefix="/api/lessons", tags=["Lessons"])


@router.get(
    "/{lesson_id}",
    response_model=LessonOut,
    summary="Lesson detail",
    description="Returns a single lesson by id.",
)
async def get_lesson(lesson_id: int, db: Annotated[AsyncSession, Depends(get_db_session)]) -> LessonOut:
    """Get lesson detail by id."""
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return LessonOut(id=lesson.id, course_id=lesson.course_id, title=lesson.title, content=lesson.content)
