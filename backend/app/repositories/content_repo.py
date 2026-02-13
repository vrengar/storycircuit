"""
Content Repository using Azure Cosmos DB SDK.
Handles database operations for content storage and retrieval.
"""

from typing import Optional, List
import uuid
from datetime import datetime, timezone
import structlog
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError
from azure.identity import DefaultAzureCredential

from ..config import Settings
from ..models.database import ContentDocument, ContentQueryResult
from ..utils.exceptions import DatabaseError, ContentNotFoundError


logger = structlog.get_logger(__name__)


class ContentRepository:
    """Repository for content database operations using Cosmos DB SDK with Azure AD auth."""
    
    def __init__(self, settings: Settings):
        """
        Initialize content repository.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        
        # Parse endpoint (remove :443 if present)
        endpoint = settings.cosmos_endpoint.rstrip('/').replace(':443', '')
        
        # Initialize Cosmos client with Azure AD credential
        # Note: Cosmos DB has disabled local key auth, so we use Azure AD
        credential = DefaultAzureCredential()
        self.client = CosmosClient(endpoint, credential)
        
        # Get database and container
        self.database = self.client.get_database_client(settings.cosmos_database)
        self.container = self.database.get_container_client(settings.cosmos_container)
        
        logger.info(
            "Cosmos DB repository initialized with Azure AD auth",
            endpoint=endpoint,
            database=settings.cosmos_database,
            container=settings.cosmos_container
        )
    
    async def create(self, document: ContentDocument) -> ContentDocument:
        """
        Create a new content document.
        
        Args:
            document: Content document to create
            
        Returns:
            Created document with database metadata
            
        Raises:
            DatabaseError: If creation fails
        """
        try:
            # Ensure ID is set
            if not document.id:
                document.id = str(uuid.uuid4())
            
            # Set timestamps
            now = datetime.now(timezone.utc)
            if not document.created_at:
                document.created_at = now
            document.updated_at = now
            
            # Convert to dict
            doc_dict = document.model_dump(mode='json', by_alias=True)
            doc_dict['id'] = document.id
            
            logger.info("Creating document in Cosmos DB", document_id=document.id, partition_key=document.partition_key)
            
            # Create document using SDK
            created_item = self.container.create_item(body=doc_dict)
            
            logger.info("Document created successfully", document_id=document.id)
            return ContentDocument(**created_item)
                
        except CosmosHttpResponseError as e:
            error_msg = f"Cosmos DB error creating document: {e.status_code} - {e.message}"
            logger.error("Document creation failed", error=error_msg, status_code=e.status_code)
            raise DatabaseError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error creating document: {str(e)}"
            logger.error("Unexpected error creating document", error=str(e))
            raise DatabaseError(error_msg)
    
    async def get_by_id(self, content_id: str, user_id: str) -> ContentDocument:
        """
        Retrieve content by ID.
        
        Args:
            content_id: Content identifier
            user_id: User identifier (partition key)
            
        Returns:
            Content document
            
        Raises:
            ContentNotFoundError: If content doesn't exist
            DatabaseError: If retrieval fails
        """
        try:
            logger.info("Getting document from Cosmos DB", document_id=content_id, user_id=user_id)
            
            # Read document using SDK
            item = self.container.read_item(item=content_id, partition_key=user_id)
            doc = ContentDocument(**item)
            
            if doc.deleted:
                raise ContentNotFoundError(f"Content {content_id} not found")
            
            return doc
                
        except CosmosResourceNotFoundError:
            logger.info("Document not found", document_id=content_id)
            raise ContentNotFoundError(f"Content {content_id} not found")
        except CosmosHttpResponseError as e:
            error_msg = f"Cosmos DB error getting document: {e.status_code} - {e.message}"
            logger.error("Document retrieval failed", error=error_msg, status_code=e.status_code)
            raise DatabaseError(error_msg)
        except ContentNotFoundError:
            raise
        except Exception as e:
            error_msg = f"Unexpected error getting document: {str(e)}"
            logger.error("Unexpected error getting document", error=str(e))
            raise DatabaseError(error_msg)
    
    async def query_by_user(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        platform: Optional[str] = None,
        sort_by: str = "date",
        order: str = "desc",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> ContentQueryResult:
        """
        Query content by user with filters and pagination.
        
        Args:
            user_id: User identifier (partition key)
            limit: Maximum number of items to return
            offset: Pagination offset
            platform: Optional platform filter
            sort_by: Sort field (date, topic)
            order: Sort order (asc, desc)
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            Query result with documents and pagination info
            
        Raises:
            DatabaseError: If query fails
        """
        try:
            # Build query
            query = "SELECT * FROM c WHERE c.userId = @userId AND c.deleted = false"
            parameters = [{"name": "@userId", "value": user_id}]
            
            if platform:
                query += " AND ARRAY_CONTAINS(c.platforms, @platform)"
                parameters.append({"name": "@platform", "value": platform})
            
            if start_date:
                query += " AND c.created_at >= @startDate"
                parameters.append({"name": "@startDate", "value": start_date.isoformat()})
            
            if end_date:
                query += " AND c.created_at <= @endDate"
                parameters.append({"name": "@endDate", "value": end_date.isoformat()})
            
            # Add sorting
            sort_field = "c.created_at" if sort_by == "date" else "c.topic"
            sort_order = "DESC" if order.lower() == "desc" else "ASC"
            query += f" ORDER BY {sort_field} {sort_order}"
            
            # Add pagination
            query += f" OFFSET {offset} LIMIT {limit}"
            
            logger.info("Querying documents from Cosmos DB", user_id=user_id, platform=platform)
            
            # Execute query using SDK
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                partition_key=user_id,
                max_item_count=limit
            ))
            
            documents = [ContentDocument(**item) for item in items]
            
            logger.info("Documents retrieved successfully", count=len(documents))
            
            return ContentQueryResult(
                documents=documents,
                count=len(documents)
            )
                
        except CosmosHttpResponseError as e:
            error_msg = f"Cosmos DB error querying documents: {e.status_code} - {e.message}"
            logger.error("Document query failed", error=error_msg, status_code=e.status_code)
            raise DatabaseError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error querying documents: {str(e)}"
            logger.error("Unexpected error querying documents", error=str(e))
            raise DatabaseError(error_msg)
    
    async def delete(self, content_id: str, user_id: str) -> None:
        """
        Soft delete content.
        
        Args:
            content_id: Content identifier
            user_id: User identifier (partition key)
            
        Raises:
            ContentNotFoundError: If content doesn't exist
            DatabaseError: If deletion fails
        """
        try:
            # Get existing document
            document = await self.get_by_id(content_id, user_id)
            
            # Mark as deleted
            document.deleted = True
            document.updated_at = datetime.now(timezone.utc)
            
            # Convert to dict
            doc_dict = document.model_dump(mode='json')
            doc_dict['id'] = document.id
            
            logger.info("Soft deleting document in Cosmos DB", document_id=content_id)
            
            # Replace document using SDK
            self.container.replace_item(item=content_id, body=doc_dict)
            
            logger.info("Document soft deleted successfully", document_id=content_id)
            
        except ContentNotFoundError:
            raise
        except CosmosHttpResponseError as e:
            error_msg = f"Cosmos DB error deleting document: {e.status_code} - {e.message}"
            logger.error("Document deletion failed", error=error_msg, status_code=e.status_code)
            raise DatabaseError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error deleting document: {str(e)}"
            logger.error("Unexpected error deleting document", error=str(e))
            raise DatabaseError(error_msg)
    
    async def health_check(self) -> bool:
        """
        Check if database is healthy.
        
        Returns:
            True if database is accessible, False otherwise
        """
        try:
            # Simple query to test connectivity
            query = "SELECT VALUE COUNT(1) FROM c"
            
            # Execute query using SDK
            list(self.container.query_items(query=query, max_item_count=1))
            
            return True
        except Exception as e:
            logger.error("Database health check failed", error=str(e))
            return False
