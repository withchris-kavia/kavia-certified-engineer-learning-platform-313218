"""Authentication routes (register/login/logout/me)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User
from app.db.session import get_db_session
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserOut

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a user with an email + password, returns the created user.",
)
async def register(payload: RegisterRequest, db: Annotated[AsyncSession, Depends(get_db_session)]) -> UserOut:
    """Register a new user account."""
    user = User(email=str(payload.email).lower(), full_name=payload.full_name, password_hash=hash_password(payload.password))
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    await db.refresh(user)
    return UserOut(id=user.id, email=user.email, full_name=user.full_name)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    description="Validates credentials and returns a JWT access token.",
)
async def login(payload: LoginRequest, db: Annotated[AsyncSession, Depends(get_db_session)]) -> TokenResponse:
    """Authenticate user and return JWT access token."""
    result = await db.execute(select(User).where(User.email == str(payload.email).lower()))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.post(
    "/logout",
    summary="Logout (placeholder)",
    description="Logout is a placeholder for stateless JWT. Clients should discard the token.",
)
async def logout() -> dict:
    """Stateless JWT logout placeholder."""
    return {"status": "ok", "detail": "Client-side logout: discard the token"}


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user",
    description="Returns the authenticated user's profile.",
)
async def me(current_user: Annotated[User, Depends(get_current_user)]) -> UserOut:
    """Return currently authenticated user."""
    return UserOut(id=current_user.id, email=current_user.email, full_name=current_user.full_name)
