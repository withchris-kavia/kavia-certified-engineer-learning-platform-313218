"""Schemas for lesson resources."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LessonOut(BaseModel):
    id: int = Field(..., description="Lesson id.")
    course_id: int = Field(..., description="Parent course id.")
    title: str = Field(..., description="Lesson title.")
    content: str | None = Field(default=None, description="Lesson content (may be long).")
