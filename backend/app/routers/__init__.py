"""
Routers package initialization.
"""

from .content import router as content_router
from .health import router as health_router

__all__ = ["content_router", "health_router"]
