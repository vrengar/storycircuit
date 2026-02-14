"""
Response models for StoryCircuit API.
Defines output schemas using Pydantic.
"""

from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from .requests import Platform


# Content Plan Models
class ContentPlan(BaseModel):
    """Content planning structure - flexible schema."""

    hook: Optional[str] = Field(None, description="Attention-grabbing opening")
    narrative_frame: Optional[str] = Field(
        None, description="Story structure framework"
    )
    key_points: Optional[list[str]] = Field(None, description="Main points to cover")
    example: Optional[str] = Field(None, description="Practical example or analogy")
    cta: Optional[str] = Field(None, description="Call-to-action")
    title: Optional[str] = Field(None, description="Plan title")
    objectives: Optional[list[str]] = Field(None, description="Content objectives")

    class Config:
        extra = "allow"  # Allow additional fields from agent


# Platform Output Models
class Tweet(BaseModel):
    """Individual tweet in a thread."""

    order: int = Field(..., description="Tweet position in thread")
    content: str = Field(..., description="Tweet text content")
    character_count: int = Field(..., description="Number of characters")


class TwitterOutput(BaseModel):
    """Twitter/X thread output."""

    thread_structure: str = Field(..., description="Thread composition description")
    tweets: list[Tweet] = Field(..., description="Individual tweets")


class LinkedInVersion(BaseModel):
    """LinkedIn post version."""

    content: str = Field(..., description="Post content in markdown")
    character_count: int = Field(..., description="Total character count")
    estimated_read_time: str = Field(..., description="Estimated reading time")


class CarouselSlide(BaseModel):
    """LinkedIn carousel slide."""

    slide_number: int = Field(..., description="Slide position")
    title: str = Field(..., description="Slide title")
    bullets: list[str] = Field(..., description="Bullet points")


class LinkedInCarousel(BaseModel):
    """LinkedIn carousel structure."""

    slides: list[CarouselSlide] = Field(..., description="Carousel slides")


class LinkedInOutput(BaseModel):
    """LinkedIn post output."""

    short_version: LinkedInVersion = Field(..., description="Concise version")
    long_version: LinkedInVersion = Field(..., description="Detailed version")
    carousel: Optional[LinkedInCarousel] = Field(None, description="Optional carousel")


class GitHubOutput(BaseModel):
    """GitHub content output."""

    readme_snippet: str = Field(..., description="README section")
    release_notes: str = Field(..., description="Release notes content")


class BlogOutput(BaseModel):
    """Blog post output."""

    content: str = Field(..., description="Full blog post in markdown")
    character_count: int = Field(..., description="Total character count")
    estimated_read_time: str = Field(..., description="Estimated reading time")


class PlatformOutputs(BaseModel):
    """Collection of platform-specific outputs - flexible structure."""

    twitter: Optional[dict[str, Any]] = None
    linkedin: Optional[dict[str, Any]] = None
    github: Optional[dict[str, Any]] = None
    blog: Optional[dict[str, Any]] = None

    class Config:
        extra = "allow"  # Allow additional platforms


# Main Content Models
class GeneratedContent(BaseModel):
    """Complete generated content structure."""

    plan: ContentPlan = Field(..., description="Content planning details")
    outputs: PlatformOutputs = Field(..., description="Platform-specific content")
    notes: str = Field(..., description="Additional notes from agent")


class ContentMetadata(BaseModel):
    """Metadata about content generation."""

    generated_at: datetime = Field(..., description="Generation timestamp")
    duration: float = Field(..., description="Generation duration in seconds")
    user_id: str = Field(..., description="User identifier")
    agent_version: str = Field(..., description="Agent version used")


class ContentGenerationResponse(BaseModel):
    """Response for content generation request."""

    id: str = Field(..., description="Unique content identifier (UUID)")
    status: str = Field(..., description="Generation status")
    content: GeneratedContent = Field(..., description="Generated content")
    metadata: ContentMetadata = Field(..., description="Generation metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "success",
                "content": {
                    "plan": {
                        "hook": "Most teams struggle with AI agent orchestration...",
                        "narrative_frame": "Problem → Solution → Implementation",
                        "key_points": [
                            "Sequential vs parallel execution",
                            "Error handling",
                        ],
                        "example": "Picture a customer support agent...",
                        "cta": "Try building your first agent",
                    },
                    "outputs": {
                        "twitter": {
                            "thread_structure": "7 tweets",
                            "tweets": [
                                {
                                    "order": 1,
                                    "content": "Thread starter...",
                                    "character_count": 138,
                                }
                            ],
                        }
                    },
                    "notes": "Agent assumed basic understanding",
                },
                "metadata": {
                    "generated_at": "2026-02-11T14:30:45.123Z",
                    "duration": 3.2,
                    "user_id": "user@example.com",
                    "agent_version": "storycircuit-v1.0",
                },
            }
        }


# History Models
class ContentHistoryItem(BaseModel):
    """Summary item in content history list."""

    id: str = Field(..., description="Content identifier")
    topic: str = Field(..., description="Content topic")
    platforms: list[Platform] = Field(..., description="Target platforms")
    generated_at: datetime = Field(..., description="Generation timestamp")
    user_id: str = Field(..., description="User identifier")
    summary: str = Field(..., description="Content summary/hook")


class PaginationInfo(BaseModel):
    """Pagination metadata."""

    total: int = Field(..., description="Total number of items")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Current offset")
    has_more: bool = Field(..., description="More items available")


class ContentHistoryResponse(BaseModel):
    """Response for content history request."""

    items: list[ContentHistoryItem] = Field(..., description="History items")
    pagination: PaginationInfo = Field(..., description="Pagination info")


# Health Check Models
class HealthResponse(BaseModel):
    """Basic health check response."""

    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")


class ServiceHealth(BaseModel):
    """Individual service health status."""

    database: str = Field(..., description="Database health")
    agent: str = Field(..., description="Agent service health")


class ReadinessResponse(BaseModel):
    """Readiness probe response."""

    status: str = Field(..., description="Readiness status")
    checks: ServiceHealth = Field(..., description="Service health checks")
    timestamp: datetime = Field(..., description="Check timestamp")


# Error Models
class ValidationError(BaseModel):
    """Validation error detail."""

    loc: list[str | int] = Field(..., description="Error location")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")


class ErrorResponse(BaseModel):
    """Error response model."""

    detail: str | list[ValidationError] = Field(..., description="Error details")
    error_code: Optional[str] = Field(None, description="Error code")
    trace_id: Optional[str] = Field(None, description="Trace identifier")
    retry_after: Optional[int] = Field(None, description="Retry after seconds")
