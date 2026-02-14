"""
Models package initialization.
Exports all model classes for easy import.
"""

from .requests import (
    Platform,
    ContentGenerationRequest,
    ContentHistoryQueryParams,
    ExportQueryParams,
)

from .responses import (
    ContentPlan,
    Tweet,
    TwitterOutput,
    LinkedInVersion,
    CarouselSlide,
    LinkedInCarousel,
    LinkedInOutput,
    GitHubOutput,
    BlogOutput,
    PlatformOutputs,
    GeneratedContent,
    ContentMetadata,
    ContentGenerationResponse,
    ContentHistoryItem,
    PaginationInfo,
    ContentHistoryResponse,
    HealthResponse,
    ServiceHealth,
    ReadinessResponse,
    ValidationError,
    ErrorResponse,
)

from .database import (
    ContentDocument,
    ContentQueryResult,
    content_to_document,
    document_to_response,
)

__all__ = [
    # Request models
    "Platform",
    "ContentGenerationRequest",
    "ContentHistoryQueryParams",
    "ExportQueryParams",
    # Response models
    "ContentPlan",
    "Tweet",
    "TwitterOutput",
    "LinkedInVersion",
    "CarouselSlide",
    "LinkedInCarousel",
    "LinkedInOutput",
    "GitHubOutput",
    "BlogOutput",
    "PlatformOutputs",
    "GeneratedContent",
    "ContentMetadata",
    "ContentGenerationResponse",
    "ContentHistoryItem",
    "PaginationInfo",
    "ContentHistoryResponse",
    "HealthResponse",
    "ServiceHealth",
    "ReadinessResponse",
    "ValidationError",
    "ErrorResponse",
    # Database models
    "ContentDocument",
    "ContentQueryResult",
    "content_to_document",
    "document_to_response",
]
