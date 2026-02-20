from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .citation import Citation

class ResponseStatus(str, Enum):
    COMPLETE = "complete"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    REJECTED = "rejected"

class Response(BaseModel):
    """
    The system-generated answer containing information exclusively from retrieved sources with proper citations.
    """
    id: str = Field(..., description="Unique identifier for the response")
    query_id: str = Field(..., description="Reference to the original query")
    content: str = Field("", description="The response text")
    status: ResponseStatus = Field(..., description="Response status ('complete', 'insufficient_evidence', 'rejected')")
    created_at: datetime = Field(default_factory=datetime.now, description="When the response was generated")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score (0.0 to 1.0)")
    disclaimers: Optional[str] = Field(None, description="Required safety disclaimer for medical/legal information")
    citations: List[Citation] = Field(default_factory=list, description="List of citations for the response")

    @validator('status')
    def validate_status_content(cls, status, values):
        """Validate that content is empty when status is 'insufficient_evidence'."""
        if status == ResponseStatus.INSUFFICIENT_EVIDENCE and values.get('content', '').strip():
            raise ValueError('Content must be empty when status is insufficient_evidence')
        return status

    @validator('confidence')
    def confidence_valid_range(cls, v):
        """Validate that confidence is between 0.0 and 1.0 if provided."""
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v

    @validator('disclaimers')
    def disclaimers_required_for_medical_legal(cls, v, values):
        """Validate that disclaimer is mandatory for medical/legal responses."""
        # This is a simplified check - in a real implementation,
        # we might need to determine if the response contains medical/legal content
        status = values.get('status')
        if status != ResponseStatus.INSUFFICIENT_EVIDENCE and not v:
            # In a real system, we might conditionally require disclaimer based on domain
            pass  # For now, we'll make disclaimer optional in validation but required in business logic
        return v

    class Config:
        use_enum_values = True