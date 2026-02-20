from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    RESEARCHER = "researcher"
    CLINICIAN = "clinician"
    LEGAL_PROFESSIONAL = "legal_professional"
    ADMIN = "admin"

class User(BaseModel):
    """
    Different types of users (researchers, clinicians, legal professionals, administrators) with appropriate access levels.
    """
    id: str = Field(..., description="Unique identifier for the user")
    username: str = Field(..., min_length=3, max_length=50, description="User's identifier")
    email: EmailStr = Field(..., description="User's email address")
    role: UserRole = Field(..., description="User role ('researcher', 'clinician', 'legal_professional', 'admin')")
    created_at: datetime = Field(default_factory=datetime.now, description="When the user account was created")
    last_access: Optional[datetime] = Field(None, description="When the user last accessed the system")

    @validator('username')
    def username_unique(cls, v):
        """In a real implementation, this would check for uniqueness in the database.
        Here we just validate format."""
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username must be at most 50 characters long')
        return v

    @validator('role')
    def role_valid(cls, v):
        """Validate that role is one of the allowed values."""
        if v not in UserRole:
            raise ValueError('Role must be one of the allowed values')
        return v

    class Config:
        use_enum_values = True