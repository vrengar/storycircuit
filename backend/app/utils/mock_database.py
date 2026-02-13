"""Mock database for local development."""

from typing import Optional
from datetime import datetime, UTC
import uuid


class MockContentRepository:
    """Mock implementation of content repository."""
    
    def __init__(self):
        self._storage = {}
    
    async def create(self, document: dict) -> dict:
        """Create a new document."""
        doc_id = document.get("id", str(uuid.uuid4()))
        document["id"] = doc_id
        document["created_at"] = datetime.now(UTC).isoformat()
        self._storage[doc_id] = document
        return document
    
    async def get(self, document_id: str) -> Optional[dict]:
        """Retrieve a document by ID."""
        return self._storage.get(document_id)
    
    async def update(self, document_id: str, document: dict) -> Optional[dict]:
        """Update an existing document."""
        if document_id in self._storage:
            document["id"] = document_id
            document["updated_at"] = datetime.now(UTC).isoformat()
            self._storage[document_id] = document
            return document
        return None
    
    async def delete(self, document_id: str) -> bool:
        """Delete a document."""
        if document_id in self._storage:
            del self._storage[document_id]
            return True
        return False
    
    async def list(self, user_id: str, limit: int = 10) -> list[dict]:
        """List documents for a user."""
        user_docs = [doc for doc in self._storage.values() if doc.get("user_id") == user_id or doc.get("userId") == user_id]
        return user_docs[:limit]
