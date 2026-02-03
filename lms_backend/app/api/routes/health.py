"""Health check endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health check", description="Basic health check endpoint.")
async def health() -> dict:
    """Return basic service health."""
    return {"status": "ok"}


@router.get("/ready", summary="Readiness probe", description="Readiness probe endpoint.")
async def ready() -> dict:
    """Return readiness status (currently always ready)."""
    return {"status": "ready"}


@router.get("/live", summary="Liveness probe", description="Liveness probe endpoint.")
async def live() -> dict:
    """Return liveness status (currently always live)."""
    return {"status": "live"}
