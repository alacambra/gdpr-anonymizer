"""Health check router."""

from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from typing import Dict, Any

from ..dependencies import get_config
from ..schemas import HealthResponse
from ....application.config import AppConfig

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(config: AppConfig = Depends(get_config)) -> HealthResponse:
    """
    Basic health check - liveness probe.

    Returns 200 if service is running.
    Used by Kubernetes liveness probe.

    Returns:
        HealthResponse with system status
    """
    return HealthResponse(
        status="healthy",
        version="0.5.0",
        llm_provider=config.llm.provider
    )


@router.get("/health/ready")
async def readiness_check(config: AppConfig = Depends(get_config)) -> Dict[str, Any]:
    """
    Readiness check - readiness probe.

    Returns 200 if service is ready to accept traffic.
    Checks:
    - Configuration loaded
    - LLM provider configured

    Used by Kubernetes readiness probe.

    Returns:
        Dict with readiness status and details
    """
    details = {
        "config_loaded": True,
        "llm_provider": config.llm.provider,
        "dependencies": {
            "llm_provider": config.llm.provider
        }
    }

    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "0.5.0",
        "details": details
    }
