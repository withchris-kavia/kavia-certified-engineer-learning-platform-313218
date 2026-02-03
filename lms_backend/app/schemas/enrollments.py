"""Schemas for enrollment operations."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EnrollmentCreateRequest(BaseModel):
    course_id: int = Field(..., description="Course to enroll into.")


class EnrollmentOut(BaseModel):
    id: int = Field(..., description="Enrollment id.")
    course_id: int = Field(..., description="Course id.")
    user_id: int = Field(..., description="User id.")
