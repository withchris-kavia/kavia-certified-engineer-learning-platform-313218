"""Assessment API routes (simple placeholder implementation)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.models.user import User
from app.db.session import get_db_session
from app.schemas.assessments import AssessmentOut, AssessmentSubmitRequest, AssessmentSubmitResponse

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])


def _default_questions_for_lesson(lesson_id: int) -> list[str]:
    """Return deterministic placeholder questions for a lesson."""
    return [
        f"Lesson {lesson_id}: What is the main idea of this lesson?",
        f"Lesson {lesson_id}: Provide one practical takeaway.",
    ]


@router.get(
    "/{lesson_id}",
    response_model=AssessmentOut,
    summary="Get assessment for lesson",
    description="Returns a placeholder assessment (question prompts) for the lesson.",
)
async def get_assessment(
    lesson_id: int,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AssessmentOut:
    """Return assessment questions for a lesson.

    Note: `db` is currently unused but included for parity and future enhancements.
    """
    _ = db
    _ = current_user
    questions = _default_questions_for_lesson(lesson_id)
    return AssessmentOut(lesson_id=lesson_id, questions=questions)


@router.post(
    "/{lesson_id}/submit",
    response_model=AssessmentSubmitResponse,
    summary="Submit assessment",
    description="Submits answers and returns a placeholder score between 0 and 1.",
)
async def submit_assessment(
    lesson_id: int,
    payload: AssessmentSubmitRequest,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AssessmentSubmitResponse:
    """Submit assessment answers and return a naive score."""
    _ = db
    _ = current_user
    questions = _default_questions_for_lesson(lesson_id)
    # Naive scoring: fraction of non-empty answers up to number of questions
    expected = len(questions)
    provided = min(len(payload.answers), expected)
    non_empty = sum(1 for a in payload.answers[:expected] if a and a.strip())
    score = non_empty / expected if expected else 0.0
    # If user sent fewer than expected, unanswered are counted as empty automatically.
    _ = provided
    return AssessmentSubmitResponse(lesson_id=lesson_id, score=float(score))
