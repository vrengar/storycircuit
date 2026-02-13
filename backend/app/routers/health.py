"""
Health check router.
Provides health and readiness endpoints for monitoring.
"""

from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, status
import structlog

from ..models.responses import HealthResponse, ReadinessResponse, ServiceHealth
from ..services.agent_service import AgentService
from ..repositories.content_repo import ContentRepository
from ..dependencies import get_agent_service, get_content_repository


logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK
)
async def health_check():
    """
    Basic health check endpoint.
    Returns application status and version.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    status_code=status.HTTP_200_OK
)
async def readiness_check(
    agent_service=Depends(get_agent_service),
    content_repo=Depends(get_content_repository)
):
    """
    Readiness probe with dependency checks.
    Checks connectivity to agent service and database.
    Returns 503 if any dependency is unhealthy.
    """
    logger.info("Performing readiness check")
    
    # Check agent service
    agent_healthy = await agent_service.health_check()
    agent_status = "healthy" if agent_healthy else "unhealthy"
    
    # Check database
    db_healthy = await content_repo.health_check()
    db_status = "healthy" if db_healthy else "unhealthy"
    
    # Determine overall status
    all_healthy = agent_healthy and db_healthy
    overall_status = "ready" if all_healthy else "not_ready"
    
    response_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    logger.info(
        "Readiness check completed",
        status=overall_status,
        agent=agent_status,
        database=db_status
    )
    
    return ReadinessResponse(
        status=overall_status,
        checks=ServiceHealth(
            database=db_status,
            agent=agent_status
        ),
        timestamp=datetime.utcnow()
    )
