"""Course API routes."""

from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.course import Course
from app.db.session import get_db_session
from app.schemas.courses import CourseOut

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.get(
    "",
    response_model=List[CourseOut],
    summary="List courses",
    description="Returns all courses.",
)
async def list_courses(db: Annotated[AsyncSession, Depends(get_db_session)]) -> List[CourseOut]:
    """List all courses."""
    result = await db.execute(select(Course).order_by(Course.id.asc()))
    courses = result.scalars().all()
    return [CourseOut(id=c.id, title=c.title, description=c.description) for c in courses]


@router.get(
    "/{course_id}",
    response_model=CourseOut,
    summary="Course detail",
    description="Returns a single course by id.",
)
async def get_course(course_id: int, db: Annotated[AsyncSession, Depends(get_db_session)]) -> CourseOut:
    """Get course detail by id."""
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return CourseOut(id=course.id, title=course.title, description=course.description)
