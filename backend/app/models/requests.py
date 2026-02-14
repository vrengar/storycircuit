"""
Request models for StoryCircuit API.
Defines input validation schemas using Pydantic.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class Platform(str, Enum):
    """Supported social media platforms."""

    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    GITHUB = "github"
    BLOG = "blog"


class ContentGenerationRequest(BaseModel):
    """Request model for content generation."""

    topic: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Technical topic to generate content about",
        examples=["Understanding AI agent orchestration patterns"],
    )

    platforms: list[Platform] = Field(
        ...,
        min_length=1,
        max_length=5,
        description="Target platforms for content generation",
        examples=[["linkedin", "twitter"]],
    )

    audience: Optional[str] = Field(
        None,
        max_length=200,
        description="Target audience description",
        examples=["software engineers", "technical architects"],
    )

    additional_context: Optional[str] = Field(
        None,
        max_length=1000,
        description="Additional context or requirements for content generation",
        examples=["Focus on Microsoft Azure AI Foundry tools"],
    )

    @field_validator("platforms")
    @classmethod
    def validate_unique_platforms(cls, v: list[Platform]) -> list[Platform]:
        """Ensure platforms list contains unique values."""
        if len(v) != len(set(v)):
            raise ValueError("Platforms must be unique")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "AI agent orchestration patterns",
                "platforms": ["linkedin", "twitter", "github"],
                "audience": "software engineers",
                "additional_context": "Focus on Microsoft Azure AI Foundry",
            }
        }


class ContentHistoryQueryParams(BaseModel):
    """Query parameters for content history endpoint."""

    limit: int = Field(20, ge=1, le=100, description="Number of items to return")

    offset: int = Field(0, ge=0, description="Pagination offset")

    platform: Optional[Platform] = Field(None, description="Filter by platform")

    sort_by: str = Field(
        "date", pattern="^(date|topic)$", description="Field to sort by"
    )

    order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")

    start_date: Optional[str] = Field(
        None,
        description="Filter by start date (ISO 8601)",
        examples=["2026-02-01T00:00:00Z"],
    )

    end_date: Optional[str] = Field(
        None,
        description="Filter by end date (ISO 8601)",
        examples=["2026-02-28T23:59:59Z"],
    )


class ExportQueryParams(BaseModel):
    """Query parameters for content export endpoint."""

    format: str = Field(
        "markdown", pattern="^(markdown|json)$", description="Export format"
    )

    platform: str = Field("all", description="Specific platform or 'all'")
