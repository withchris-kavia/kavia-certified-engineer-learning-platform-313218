"""Schemas for course resources."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CourseOut(BaseModel):
    id: int = Field(..., description="Course id.")
    title: str = Field(..., description="Course title.")
    description: str | None = Field(default=None, description="Course description.")
