"""
Database models for StoryCircuit.
Defines data structures for Cosmos DB storage.
"""

from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from .requests import Platform


class ContentDocument(BaseModel):
    """
    Cosmos DB document model for storing generated content.
    Maps to 'ContentGenerations' container.
    """

    # Document identity (Cosmos DB required fields)
    id: str = Field(..., description="Unique document ID (UUID)")
    partition_key: str = Field(
        ..., alias="partitionKey", description="Partition key (userId)"
    )
    user_id: str = Field(
        ..., alias="userId", description="User identifier (same as partition key)"
    )

    # Content details
    topic: str = Field(..., description="Content topic")
    platforms: list[str] = Field(..., description="Target platforms")

    # Generated content (stored as nested JSON)
    generated_content: dict[str, Any] = Field(
        ...,
        alias="generatedContent",
        description="Complete generated content structure",
    )

    # Metadata
    metadata: dict[str, Any] = Field(..., description="Generation metadata")

    # Audit fields
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        alias="createdAt",
        description="Document creation timestamp",
    )

    updated_at: Optional[datetime] = Field(
        None, alias="updatedAt", description="Last update timestamp"
    )

    deleted: bool = Field(default=False, description="Soft delete flag")

    # Cosmos DB system fields (populated by database)
    _rid: Optional[str] = None
    _self: Optional[str] = None
    _etag: Optional[str] = None
    _attachments: Optional[str] = None
    _ts: Optional[int] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "partitionKey": "user@example.com",
                "topic": "AI agent orchestration patterns",
                "platforms": ["linkedin", "twitter"],
                "generatedContent": {
                    "plan": {
                        "hook": "Most teams struggle...",
                        "narrativeFrame": "Problem → Solution",
                        "keyPoints": ["Point 1", "Point 2"],
                        "example": "Example text",
                        "cta": "Call to action",
                    },
                    "outputs": {
                        "twitter": {"threadStructure": "5 tweets", "tweets": []}
                    },
                    "notes": "Additional notes",
                },
                "metadata": {
                    "userId": "user@example.com",
                    "timestamp": "2026-02-11T14:30:45.123Z",
                    "agentVersion": "storycircuit-v1.0",
                    "duration": 3.2,
                },
                "createdAt": "2026-02-11T14:30:45.123Z",
                "deleted": False,
            }
        }


class ContentQueryResult(BaseModel):
    """Result from content query with pagination."""

    documents: list[ContentDocument]
    continuation_token: Optional[str] = None
    count: int


# Helper functions for database operations


def content_to_document(
    content_id: str,
    user_id: str,
    topic: str,
    platforms: list[Platform],
    generated_content: dict[str, Any],
    metadata: dict[str, Any],
) -> ContentDocument:
    """
    Convert content generation result to database document.

    Args:
        content_id: Unique content identifier
        user_id: User identifier (used as partition key)
        topic: Content topic
        platforms: List of target platforms
        generated_content: Generated content structure
        metadata: Generation metadata

    Returns:
        ContentDocument ready for database insertion
    """
    return ContentDocument(
        id=content_id,
        partition_key=user_id,
        user_id=user_id,
        topic=topic,
        platforms=[p.value if isinstance(p, Platform) else p for p in platforms],
        generated_content=generated_content,
        metadata=metadata,
    )


def document_to_response(document: ContentDocument) -> dict[str, Any]:
    """
    Convert database document to API response format.

    Args:
        document: Cosmos DB document

    Returns:
        Dictionary formatted for API response
    """
    return {
        "id": document.id,
        "topic": document.topic,
        "platforms": document.platforms,
        "content": document.generated_content,
        "metadata": document.metadata,
        "created_at": document.created_at.isoformat() if document.created_at else None,
    }
