"""FastAPI dependencies for database and authentication."""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import try_get_subject
from app.db.models.user import User
from app.db.session import get_db_session

_bearer = HTTPBearer(auto_error=False)


# PUBLIC_INTERFACE
async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(_bearer)],
) -> User:
    """Return the current authenticated user based on Bearer JWT token."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    subject = try_get_subject(credentials.credentials)
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    try:
        user_id = int(subject)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
