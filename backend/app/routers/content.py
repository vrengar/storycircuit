"""
Content API router.
Handles content generation, history, and management endpoints.
"""

from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from fastapi.responses import PlainTextResponse, JSONResponse
import structlog

from ..models.requests import ContentGenerationRequest, Platform
from ..models.responses import (
    ContentGenerationResponse,
    ContentHistoryResponse,
    ErrorResponse
)
from ..services.content_service import ContentService
from ..services.export_service import ExportService
from ..utils.exceptions import (
    AgentServiceError,
    AgentTimeoutError,
    DatabaseError,
    ContentNotFoundError,
    ExportError
)
from ..dependencies import get_content_service, get_export_service
from ..utils.security import ContentSecurityValidator


logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/content", tags=["content"])


# Dependency injection helpers
def get_user_id() -> str:
    """
    Get current user ID.
    In production, this would extract from JWT token.
    For development, return a default user.
    """
    # TODO: Extract from authentication token in production
    return "dev-user@example.com"


@router.post(
    "/generate",
    response_model=ContentGenerationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        502: {"model": ErrorResponse, "description": "Agent service error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    }
)
async def generate_content(
    request: ContentGenerationRequest,
    user_id: Annotated[str, Depends(get_user_id)],
    content_service=Depends(get_content_service),
):
    """
    Generate platform-optimized content from a technical topic.
    
    - **topic**: Technical topic to generate content about (3-500 characters)
    - **platforms**: List of target platforms (1-5 platforms)
    - **audience**: Optional target audience description
    - **additional_context**: Optional additional context or requirements
    
    Returns structured content with plan, platform outputs, and notes.
    """
    try:
        # Security validation
        is_valid, error_msg = ContentSecurityValidator.validate_content_request(
            topic=request.topic,
            platforms=[p.value for p in request.platforms]
        )
        if not is_valid:
            logger.warning(
                "Content request blocked by security validation",
                user_id=user_id,
                reason=error_msg
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Security validation failed: {error_msg}"
            )
        
        logger.info(
            "Content generation request received",
            topic=request.topic,
            platforms=[p.value for p in request.platforms],
            user_id=user_id
        )
        
        result = await content_service.generate_content(
            topic=request.topic,
            platforms=request.platforms,
            user_id=user_id,
            audience=request.audience,
            additional_context=request.additional_context
        )
        
        return result
        
    except AgentTimeoutError as e:
        logger.error("Agent timeout", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=str(e)
        )
    except AgentServiceError as e:
        logger.error("Agent service error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Agent service temporarily unavailable. Please try again."
        )
    except DatabaseError as e:
        logger.error("Database error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database temporarily unavailable. Please try again."
        )
    except Exception as e:
        logger.error("Unexpected error in content generation", error=str(e), error_type=type(e).__name__, traceback=str(e.__traceback__))
        # Include error details in development
        import traceback
        error_detail = f"An unexpected error occurred: {type(e).__name__}: {str(e)}"
        logger.error("Full traceback", traceback=traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )


@router.get(
    "/history",
    response_model=ContentHistoryResponse,
    status_code=status.HTTP_200_OK
)
async def get_content_history(
    user_id: Annotated[str, Depends(get_user_id)],
    content_service=Depends(get_content_service),
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    platform: Optional[Platform] = None,
    sort_by: Annotated[str, Query(pattern="^(date|topic)$")] = "date",
    order: Annotated[str, Query(pattern="^(asc|desc)$")] = "desc",
):
    """
    Retrieve content generation history.
    
    - **limit**: Number of items to return (1-100, default: 20)
    - **offset**: Pagination offset (default: 0)
    - **platform**: Optional platform filter
    - **sort_by**: Sort field - 'date' or 'topic' (default: 'date')
    - **order**: Sort order - 'asc' or 'desc' (default: 'desc')
    """
    try:
        logger.info(
            "Content history request",
            user_id=user_id,
            limit=limit,
            offset=offset,
            platform=platform
        )
        
        result = await content_service.get_content_history(
            user_id=user_id,
            limit=limit,
            offset=offset,
            platform=platform.value if platform else None,
            sort_by=sort_by,
            order=order
        )
        
        return result
        
    except DatabaseError as e:
        logger.error("Database error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database temporarily unavailable."
        )
    except Exception as e:
        logger.error("Unexpected error retrieving history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.get(
    "/{content_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Content not found"}
    }
)
async def get_content_by_id(
    content_id: str,
    user_id: Annotated[str, Depends(get_user_id)],
    content_service=Depends(get_content_service)
):
    """
    Retrieve specific content by ID.
    
    - **content_id**: Unique content identifier
    """
    try:
        logger.info("Content retrieval request", content_id=content_id, user_id=user_id)
        
        result = await content_service.get_content_by_id(content_id, user_id)
        return result
        
    except ContentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content {content_id} not found"
        )
    except DatabaseError as e:
        logger.error("Database error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database temporarily unavailable."
        )
    except Exception as e:
        logger.error("Unexpected error retrieving content", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.get(
    "/{content_id}/export",
    status_code=status.HTTP_200_OK
)
async def export_content(
    content_id: str,
    user_id: Annotated[str, Depends(get_user_id)],
    content_service=Depends(get_content_service),
    export_service=Depends(get_export_service),
    format: Annotated[str, Query(pattern="^(markdown|json)$")] = "markdown",
    platform: str = "all"
):
    """
    Export content in specified format.
    
    - **content_id**: Unique content identifier
    - **format**: Export format - 'markdown' or 'json' (default: 'markdown')
    - **platform**: Specific platform or 'all' (default: 'all')
    """
    try:
        logger.info(
            "Content export request",
            content_id=content_id,
            format=format,
            platform=platform
        )
        
        # Get content
        content_data = await content_service.get_content_by_id(content_id, user_id)
        
        # Generate filename
        filename = export_service.get_filename(content_id, format, platform)
        
        # Export in requested format
        if format == "markdown":
            exported = export_service.export_as_markdown(
                content=content_data["content"],
                topic=content_data["topic"],
                platforms=content_data["platforms"],
                platform_filter=platform
            )
            return PlainTextResponse(
                content=exported,
                media_type="text/markdown",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        else:  # json
            exported = export_service.export_as_json(
                content_id=content_id,
                topic=content_data["topic"],
                platforms=content_data["platforms"],
                content=content_data["content"],
                metadata=content_data["metadata"],
                platform_filter=platform
            )
            return JSONResponse(
                content=exported,
                media_type="application/json",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        
    except ContentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content {content_id} not found"
        )
    except ExportError as e:
        logger.error("Export error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export content."
        )
    except Exception as e:
        logger.error("Unexpected error exporting content", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )


@router.delete(
    "/{content_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Content not found"}
    }
)
async def delete_content(
    content_id: str,
    user_id: Annotated[str, Depends(get_user_id)],
    content_service=Depends(get_content_service)
):
    """
    Delete specific content (soft delete).
    
    - **content_id**: Unique content identifier
    """
    try:
        logger.info("Content deletion request", content_id=content_id, user_id=user_id)
        
        await content_service.delete_content(content_id, user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    except ContentNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content {content_id} not found"
        )
    except DatabaseError as e:
        logger.error("Database error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database temporarily unavailable."
        )
    except Exception as e:
        logger.error("Unexpected error deleting content", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
