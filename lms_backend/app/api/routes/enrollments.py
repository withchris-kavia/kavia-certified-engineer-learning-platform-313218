"""Enrollment API routes."""

from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.models.course import Course
from app.db.models.enrollment import Enrollment
from app.db.models.user import User
from app.db.session import get_db_session
from app.schemas.enrollments import EnrollmentCreateRequest, EnrollmentOut

router = APIRouter(prefix="/api/enrollments", tags=["Enrollments"])


@router.post(
    "",
    response_model=EnrollmentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Enroll in a course",
    description="Enroll the current user into a course.",
)
async def enroll(
    payload: EnrollmentCreateRequest,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> EnrollmentOut:
    """Create an enrollment for the current user."""
    # Ensure course exists
    result = await db.execute(select(Course).where(Course.id == payload.course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    enrollment = Enrollment(user_id=current_user.id, course_id=payload.course_id)
    db.add(enrollment)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Already enrolled")
    await db.refresh(enrollment)
    return EnrollmentOut(id=enrollment.id, course_id=enrollment.course_id, user_id=enrollment.user_id)


@router.get(
    "/me",
    response_model=List[EnrollmentOut],
    summary="List my enrollments",
    description="List courses the current user is enrolled in.",
)
async def list_my_enrollments(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> List[EnrollmentOut]:
    """List enrollments for current user."""
    result = await db.execute(select(Enrollment).where(Enrollment.user_id == current_user.id).order_by(Enrollment.id.asc()))
    enrollments = result.scalars().all()
    return [EnrollmentOut(id=e.id, course_id=e.course_id, user_id=e.user_id) for e in enrollments]
