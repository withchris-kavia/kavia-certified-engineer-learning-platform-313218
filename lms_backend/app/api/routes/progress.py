"""Progress API routes."""

from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.models.lesson import Lesson
from app.db.models.progress import LessonProgress
from app.db.models.user import User
from app.db.session import get_db_session
from app.schemas.progress import LessonProgressOut, ProgressSummaryOut, ProgressUpsertRequest

router = APIRouter(prefix="/api/progress", tags=["Progress"])


@router.get(
    "/me",
    response_model=ProgressSummaryOut,
    summary="My progress summary",
    description="Returns a simple summary of tracked and completed lessons for the current user.",
)
async def my_progress_summary(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ProgressSummaryOut:
    """Return progress summary for current user."""
    total_stmt = select(func.count(LessonProgress.id)).where(LessonProgress.user_id == current_user.id)
    completed_stmt = select(func.count(LessonProgress.id)).where(
        LessonProgress.user_id == current_user.id, LessonProgress.completed.is_(True)
    )

    total = (await db.execute(total_stmt)).scalar_one()
    completed = (await db.execute(completed_stmt)).scalar_one()

    return ProgressSummaryOut(total_lessons_tracked=int(total), completed_lessons=int(completed))


@router.post(
    "",
    response_model=LessonProgressOut,
    status_code=status.HTTP_200_OK,
    summary="Upsert lesson progress",
    description="Creates or updates progress for a lesson for the current user.",
)
async def upsert_progress(
    payload: ProgressUpsertRequest,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> LessonProgressOut:
    """Upsert lesson progress for current user."""
    # Ensure lesson exists
    lesson = (await db.execute(select(Lesson).where(Lesson.id == payload.lesson_id))).scalar_one_or_none()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Try update existing
    existing = (
        await db.execute(
            select(LessonProgress).where(
                LessonProgress.user_id == current_user.id, LessonProgress.lesson_id == payload.lesson_id
            )
        )
    ).scalar_one_or_none()

    if existing:
        existing.completed = payload.completed
        await db.commit()
        await db.refresh(existing)
        return LessonProgressOut(lesson_id=existing.lesson_id, completed=existing.completed, updated_at=existing.updated_at)

    # Else insert new
    progress = LessonProgress(user_id=current_user.id, lesson_id=payload.lesson_id, completed=payload.completed)
    db.add(progress)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # Extremely rare race: fallback to select and return
        progress = (
            await db.execute(
                select(LessonProgress).where(
                    LessonProgress.user_id == current_user.id, LessonProgress.lesson_id == payload.lesson_id
                )
            )
        ).scalar_one()
    await db.refresh(progress)
    return LessonProgressOut(lesson_id=progress.lesson_id, completed=progress.completed, updated_at=progress.updated_at)
