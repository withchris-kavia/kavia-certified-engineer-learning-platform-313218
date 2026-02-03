"""Schemas for lesson progress tracking."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ProgressUpsertRequest(BaseModel):
    lesson_id: int = Field(..., description="Lesson id to update progress for.")
    completed: bool = Field(default=False, description="Whether the lesson is completed.")


class LessonProgressOut(BaseModel):
    lesson_id: int = Field(..., description="Lesson id.")
    completed: bool = Field(..., description="Completion state.")
    updated_at: datetime = Field(..., description="Last updated time.")


class ProgressSummaryOut(BaseModel):
    total_lessons_tracked: int = Field(..., description="Number of lessons with progress records.")
    completed_lessons: int = Field(..., description="Number of completed lessons.")
