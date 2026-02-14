"""
StoryCircuit FastAPI Application.
Main application entry point with dependency injection and routing.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import structlog

from .config import get_settings
from .utils import configure_logging
from .utils.security import SecurityHeaders
from .utils.exceptions import (
    StoryCircuitError,
    AgentServiceError,
    AgentTimeoutError,
    DatabaseError,
    ContentNotFoundError,
    ValidationError as AppValidationError,
    ExportError,
    RateLimitError,
)

# Import dependencies from dedicated file
from . import dependencies
from .routers import content_router, health_router

# Get settings
settings = get_settings()

# Configure logging
configure_logging(settings.log_level)
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting StoryCircuit application", environment=settings.environment)

    # Startup
    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down StoryCircuit application")


# Create FastAPI app
app = FastAPI(
    title="StoryCircuit API",
    description="Technical Narrative Architect Agent - Transform technical topics into platform-optimized social content",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)

    # Add security headers
    for header_name, header_value in SecurityHeaders.get_headers().items():
        response.headers[header_name] = header_value

    return response


# Note: Dependency injection functions are defined in dependencies.py
# They are used in routers via Depends(get_service_function)


# Exception Handlers
@app.exception_handler(AgentTimeoutError)
async def agent_timeout_handler(request: Request, exc: AgentTimeoutError):
    """Handle agent timeout errors."""
    logger.error("Agent timeout", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={"detail": str(exc), "error_code": "AGENT_TIMEOUT", "retry_after": 10},
    )


@app.exception_handler(AgentServiceError)
async def agent_service_error_handler(request: Request, exc: AgentServiceError):
    """Handle agent service errors."""
    logger.error("Agent service error", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "detail": "Agent service temporarily unavailable. Please try again.",
            "error_code": "AGENT_UNAVAILABLE",
            "retry_after": 30,
        },
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    """Handle database errors."""
    logger.error("Database error", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Database temporarily unavailable. Please try again.",
            "error_code": "DATABASE_ERROR",
            "retry_after": 10,
        },
    )


@app.exception_handler(ContentNotFoundError)
async def content_not_found_handler(request: Request, exc: ContentNotFoundError):
    """Handle content not found errors."""
    logger.warning("Content not found", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc), "error_code": "NOT_FOUND"},
    )


@app.exception_handler(RateLimitError)
async def rate_limit_handler(request: Request, exc: RateLimitError):
    """Handle rate limit errors."""
    logger.warning("Rate limit exceeded", path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "Rate limit exceeded. Please try again later.",
            "error_code": "RATE_LIMITED",
            "retry_after": 60,
        },
    )


@app.exception_handler(StoryCircuitError)
async def general_error_handler(request: Request, exc: StoryCircuitError):
    """Handle general application errors."""
    logger.error("Application error", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An error occurred. Please try again.",
            "error_code": "INTERNAL_ERROR",
        },
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(
        "Unexpected error",
        error=str(exc),
        error_type=type(exc).__name__,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred. Please contact support.",
            "error_code": "INTERNAL_ERROR",
        },
    )


# Include routers
app.include_router(content_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")

# Mount static files
import os
from pathlib import Path

# Get frontend files path - works for both local dev and container
FRONTEND_DIR = Path(__file__).parent.parent.parent / "frontend"
# In container, frontend is at /app/frontend, so adjust path
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

if FRONTEND_DIR.exists():
    # Mount CSS and JS as static files
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# Root endpoint - serve frontend
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - serves frontend index.html."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    else:
        # Fallback if frontend not available
        return {
            "message": "StoryCircuit API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/v1/health",
        }


# Add this import at the top
from fastapi import Depends


# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests."""
    logger.info(
        "Request received",
        method=request.method,
        path=request.url.path,
        client=request.client.host if request.client else None,
    )

    response = await call_next(request)

    logger.info(
        "Request completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
    )

    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
    )
