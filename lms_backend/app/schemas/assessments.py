"""Schemas for assessments (simple placeholder scoring)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AssessmentOut(BaseModel):
    lesson_id: int = Field(..., description="Lesson id.")
    questions: list[str] = Field(..., description="List of question prompts for the lesson.")


class AssessmentSubmitRequest(BaseModel):
    answers: list[str] = Field(..., description="Answers submitted by the user (parallel to questions).")


class AssessmentSubmitResponse(BaseModel):
    lesson_id: int = Field(..., description="Lesson id.")
    score: float = Field(..., ge=0, le=1, description="Score between 0 and 1.")
