"""Security primitives: password hashing and JWT helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return _pwd_context.hash(password)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    return _pwd_context.verify(plain_password, hashed_password)


# PUBLIC_INTERFACE
def create_access_token(subject: str, expires_minutes: Optional[int] = None, extra_claims: Optional[Dict[str, Any]] = None) -> str:
    """Create a signed JWT access token.

    Args:
        subject: Typically the user id (string).
        expires_minutes: Optional custom expiration minutes.
        extra_claims: Optional extra JWT claims.

    Returns:
        Signed JWT string.
    """
    expire_delta = timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    expire_at = datetime.now(timezone.utc) + expire_delta

    to_encode: Dict[str, Any] = {"sub": subject, "exp": expire_at}
    if extra_claims:
        to_encode.update(extra_claims)

    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


# PUBLIC_INTERFACE
def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token.

    Raises:
        jose.JWTError if invalid/expired.
    """
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


# PUBLIC_INTERFACE
def try_get_subject(token: str) -> Optional[str]:
    """Return the token subject if token is valid; otherwise None."""
    try:
        payload = decode_token(token)
        return payload.get("sub")
    except JWTError:
        return None
