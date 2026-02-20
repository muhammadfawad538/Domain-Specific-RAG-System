from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class QueryStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    REJECTED = "rejected"

class QueryDomain(str, Enum):
    MEDICAL = "medical"
    LEGAL = "legal"
    UNKNOWN = "unknown"

class Query(BaseModel):
    """
    A natural language question submitted by a user, including metadata about domain classification.
    """
    id: str = Field(..., description="Unique identifier for the query")
    content: str = Field(..., min_length=1, description="The natural language question text")
    domain: QueryDomain = Field(QueryDomain.UNKNOWN, description="Classification as 'medical', 'legal', or 'unknown'")
    user_id: str = Field(..., description="Reference to the user who submitted the query")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the query was submitted")
    status: QueryStatus = Field(QueryStatus.PENDING, description="Query processing status")

    @validator('content')
    def content_not_empty(cls, v):
        """Validate that content is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError('Content must not be empty')
        return v.strip()

    @validator('timestamp')
    def timestamp_in_past(cls, v):
        """Validate that timestamp is current or past time."""
        if v and v > datetime.now():
            raise ValueError('Timestamp must be current or past time')
        return v

    class Config:
        use_enum_values = True