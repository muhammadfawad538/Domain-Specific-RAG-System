from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class Chunk(BaseModel):
    """
    A semantic passage extracted from a document, used for retrieval.
    """
    id: str = Field(..., description="Unique identifier for the chunk")
    document_id: str = Field(..., description="Reference to the source document")
    content: str = Field(..., min_length=1, description="The text content of the chunk")
    chunk_index: int = Field(..., ge=0, description="Sequential position within the document")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the chunk content")
    semantic_boundary: Optional[str] = Field(None, description="Indicator of semantic completeness")
    created_at: datetime = Field(default_factory=datetime.now, description="When the chunk was created")

    @validator('content')
    def content_not_empty(cls, v):
        """Validate that content is not empty."""
        if not v or not v.strip():
            raise ValueError('Content must not be empty')
        return v.strip()

    @validator('chunk_index')
    def chunk_index_valid(cls, v):
        """Validate that chunk index is non-negative."""
        if v < 0:
            raise ValueError('Chunk index must be non-negative')
        return v

    @validator('embedding')
    def embedding_dimensions_valid(cls, v):
        """Validate that if embedding exists, it has proper dimensions."""
        if v is not None and len(v) == 0:
            raise ValueError('Embedding must have at least one dimension if provided')
        return v

    class Config:
        # Additional configuration if needed
        pass