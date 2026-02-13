"""
Shared dependency injection functions.
"""

from fastapi import Depends


# Import  settings
def get_settings():
    """Get settings instance."""
    from .config import get_settings as _get_settings
    return _get_settings()


# Service dependencies
def get_agent_service():
    """Provide AgentService instance (or mock)."""
    settings = get_settings()
    if settings.use_mock_services:
        from .utils.mock_services import MockAgentService
        return MockAgentService(settings)
    from .services import AgentService
    return AgentService(settings)


def get_content_repository():
    """Provide ContentRepository instance (or mock)."""
    settings = get_settings()
    if settings.use_mock_database:
        from .utils.mock_database import MockContentRepository
        return MockContentRepository()
    from .repositories import ContentRepository
    return ContentRepository(settings)


def get_export_service():
    """Provide ExportService instance."""
    from .services import ExportService
    return ExportService()


def get_content_service(
    agent_service=Depends(get_agent_service),
    content_repo=Depends(get_content_repository)
):
    """Provide ContentService instance."""
    from .services import ContentService
    settings = get_settings()
    return ContentService(agent_service, content_repo, settings)


# User dependency (for auth - returns dev user for now)
def get_user_id() -> str:
    """
    Get current user ID.
    In production, this would extract from JWT token.
    For development, return a default user.
    """
    return "dev-user@example.com"
