"""Health check router."""

from fastapi import APIRouter, Depends

from ..dependencies import get_config
from ..schemas import HealthResponse
from ....application.config import AppConfig

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(config: AppConfig = Depends(get_config)) -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse with system status
    """
    return HealthResponse(
        status="healthy",
        version="0.4.0",
        llm_provider=config.llm.provider
    )
