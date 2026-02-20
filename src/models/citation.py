from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Citation(BaseModel):
    """
    A reference linking a specific claim in the response to the exact source document and location.
    """
    id: str = Field(..., description="Unique identifier for the citation")
    response_id: str = Field(..., description="Reference to the response containing the citation")
    chunk_id: str = Field(..., description="Reference to the source chunk")
    document_id: str = Field(..., description="Reference to the source document")
    claim_text: str = Field(..., min_length=1, description="The specific text in the response that is being cited")
    citation_text: str = Field(..., min_length=1, description="The corresponding text in the source document")
    document_title: Optional[str] = Field(None, description="Title of the source document")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence in the citation's accuracy (0.0 to 1.0)")
    created_at: datetime = Field(default_factory=datetime.now, description="When the citation was created")

    @validator('claim_text', 'citation_text')
    def text_not_empty(cls, v):
        """Validate that text fields are not empty."""
        if not v or not v.strip():
            raise ValueError('Text fields must not be empty')
        return v.strip()

    @validator('confidence')
    def confidence_valid_range(cls, v):
        """Validate that confidence is between 0.0 and 1.0 if provided."""
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v

    class Config:
        # Additional configuration if needed
        pass