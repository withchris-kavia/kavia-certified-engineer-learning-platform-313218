"""Pydantic schemas for authentication."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address (unique).")
    password: str = Field(..., min_length=8, description="User password (min 8 chars).")
    full_name: str | None = Field(default=None, description="Optional full name.")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address.")
    password: str = Field(..., description="User password.")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token.")
    token_type: str = Field(default="bearer", description="Token type.")


class UserOut(BaseModel):
    id: int = Field(..., description="User id.")
    email: EmailStr = Field(..., description="User email.")
    full_name: str | None = Field(default=None, description="User full name.")
