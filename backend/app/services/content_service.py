"""
Content Service.
Orchestrates content generation business logic.
"""

import uuid
from datetime import datetime
from typing import Optional
import structlog

from ..config import Settings
from ..models.requests import Platform
from ..models.database import content_to_document
from ..services.agent_service import AgentService
from ..repositories.content_repo import ContentRepository
from ..utils.exceptions import AgentServiceError, DatabaseError


logger = structlog.get_logger(__name__)


class ContentService:
    """Service for content generation orchestration."""
    
    def __init__(
        self,
        agent_service: AgentService,
        content_repo: ContentRepository,
        settings: Settings
    ):
        """
        Initialize content service.
        
        Args:
            agent_service: Agent service instance
            content_repo: Content repository instance
            settings: Application settings
        """
        self.agent_service = agent_service
        self.content_repo = content_repo
        self.settings = settings
    
    async def generate_content(
        self,
        topic: str,
        platforms: list[Platform],
        user_id: str,
        audience: Optional[str] = None,
        additional_context: Optional[str] = None,
    ) -> dict:
        """
        Generate content and save to database.
        
        Args:
            topic: Technical topic
            platforms: Target platforms
            user_id: User identifier
            audience: Optional target audience
            additional_context: Optional additional context
            
        Returns:
            Dictionary with content ID, status, content, and metadata
            
        Raises:
            AgentServiceError: If content generation fails
            DatabaseError: If database save fails
        """
        content_id = str(uuid.uuid4())
        
        logger.info(
            "Starting content generation",
            content_id=content_id,
            topic=topic,
            platforms=[p.value for p in platforms],
            user_id=user_id
        )
        
        try:
            # Generate content with agent
            result = await self.agent_service.generate_content(
                topic=topic,
                platforms=[p.value for p in platforms],
                audience=audience,
                additional_context=additional_context
            )
            
            generated_content = result["content"]
            duration = result["duration"]
            
            # Prepare metadata
            metadata = {
                "userId": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "agentVersion": "storycircuit-v1.0",
                "duration": duration
            }
            
            # Save to database
            document = content_to_document(
                content_id=content_id,
                user_id=user_id,
                topic=topic,
                platforms=platforms,
                generated_content=generated_content,
                metadata=metadata
            )
            
            # Save document to database (pass the ContentDocument object, not dict)
            await self.content_repo.create(document)
            
            logger.info(
                "Content generation completed",
                content_id=content_id,
                duration=duration
            )
            
            # Return response
            return {
                "id": content_id,
                "status": "success",
                "content": generated_content,
                "metadata": {
                    "generated_at": datetime.utcnow(),
                    "duration": duration,
                    "user_id": user_id,
                    "agent_version": "storycircuit-v1.0"
                }
            }
            
        except AgentServiceError as e:
            logger.error("Agent service error", error=str(e), content_id=content_id)
            raise
        except DatabaseError as e:
            logger.error("Database error", error=str(e), content_id=content_id)
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during content generation",
                error=str(e),
                content_id=content_id
            )
            raise
    
    async def get_content_history(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        platform: Optional[str] = None,
        sort_by: str = "date",
        order: str = "desc",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> dict:
        """
        Retrieve content history for user.
        
        Args:
            user_id: User identifier
            limit: Maximum items to return
            offset: Pagination offset
            platform: Optional platform filter
            sort_by: Sort field
            order: Sort order
            start_date: Optional start date
            end_date: Optional end date
            
        Returns:
            Dictionary with items and pagination info
        """
        logger.info(
            "Retrieving content history",
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        result = await self.content_repo.query_by_user(
            user_id=user_id,
            limit=limit,
            offset=offset,
            platform=platform,
            sort_by=sort_by,
            order=order,
            start_date=start_date,
            end_date=end_date
        )
        
        # Convert documents to history items
        items = []
        for doc in result.documents:
            # Extract summary (hook from plan)
            summary = "Content generated"
            if "plan" in doc.generated_content and "hook" in doc.generated_content["plan"]:
                summary = doc.generated_content["plan"]["hook"][:200]
            
            items.append({
                "id": doc.id,
                "topic": doc.topic,
                "platforms": doc.platforms,
                "generated_at": doc.created_at,
                "user_id": doc.partition_key,
                "summary": summary
            })
        
        return {
            "items": items,
            "pagination": {
                "total": result.count,
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < result.count
            }
        }
    
    async def get_content_by_id(self, content_id: str, user_id: str) -> dict:
        """
        Retrieve specific content by ID.
        
        Args:
            content_id: Content identifier
            user_id: User identifier
            
        Returns:
            Dictionary with content details
        """
        logger.info("Retrieving content", content_id=content_id, user_id=user_id)
        
        document = await self.content_repo.get_by_id(content_id, user_id)
        
        return {
            "id": document.id,
            "topic": document.topic,
            "platforms": document.platforms,
            "content": document.generated_content,
            "metadata": document.metadata
        }
    
    async def delete_content(self, content_id: str, user_id: str) -> None:
        """
        Delete content.
        
        Args:
            content_id: Content identifier
            user_id: User identifier
        """
        logger.info("Deleting content", content_id=content_id, user_id=user_id)
        await self.content_repo.delete(content_id, user_id)
