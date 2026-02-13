"""
Custom exceptions for StoryCircuit application.
"""


class StoryCircuitError(Exception):
    """Base exception for StoryCircuit application."""
    pass


class AgentServiceError(StoryCircuitError):
    """Exception raised when agent service fails."""
    pass


class AgentTimeoutError(AgentServiceError):
    """Exception raised when agent request times out."""
    pass


class DatabaseError(StoryCircuitError):
    """Exception raised when database operation fails."""
    pass


class ContentNotFoundError(StoryCircuitError):
    """Exception raised when content is not found."""
    pass


class ValidationError(StoryCircuitError):
    """Exception raised for validation errors."""
    pass


class ExportError(StoryCircuitError):
    """Exception raised when export operation fails."""
    pass


class AuthenticationError(StoryCircuitError):
    """Exception raised for authentication failures."""
    pass


class AuthorizationError(StoryCircuitError):
    """Exception raised for authorization failures."""
    pass


class RateLimitError(StoryCircuitError):
    """Exception raised when rate limit is exceeded."""
    pass
