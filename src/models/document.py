from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class DocumentDomain(str, Enum):
    MEDICAL = "medical"
    LEGAL = "legal"
    MIXED = "mixed"

class FileFormat(str, Enum):
    PDF = "PDF"
    TEXT = "TEXT"
    DOC = "DOC"
    DOCX = "DOCX"

class Document(BaseModel):
    """
    A vetted source file (PDF or text) containing medical or legal information with associated metadata.
    """
    id: str = Field(..., description="Unique identifier for the document")
    title: str = Field(..., min_length=1, description="Document title")
    author: str = Field(..., description="Document author")
    publication: Optional[str] = Field(None, description="Publication source or venue")
    year: int = Field(..., ge=1900, le=2030, description="Publication year")
    file_path: str = Field(..., description="Path to stored file")
    file_format: FileFormat = Field(..., description="File format ('PDF', 'TEXT', or others)")
    checksum: Optional[str] = Field(None, description="File integrity verification")
    domain: DocumentDomain = Field(..., description="'medical', 'legal', or 'mixed'")
    created_at: datetime = Field(default_factory=datetime.now, description="When the document was added to the system")
    uploaded_by: str = Field(..., description="User who uploaded the document")
    chunk_count: int = Field(0, ge=0, description="Number of semantic chunks derived from the document")

    @validator('title')
    def title_not_empty(cls, v):
        """Validate that title is not empty."""
        if not v or not v.strip():
            raise ValueError('Title must not be empty')
        return v.strip()

    @validator('year')
    def year_valid(cls, v):
        """Validate that year is within a reasonable range."""
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 1:
            raise ValueError(f'Year must be between 1900 and {current_year + 1}')
        return v

    @validator('file_format')
    def file_format_valid(cls, v):
        """Validate that file format is one of the allowed values."""
        if v not in FileFormat:
            raise ValueError('File format must be one of the allowed values')
        return v

    class Config:
        use_enum_values = True