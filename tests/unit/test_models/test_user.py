import pytest
from datetime import datetime
from src.models.user import User, UserRole


def test_user_creation():
    """Test successful creation of a User object."""
    user = User(
        id="user_id",
        username="test_user",
        email="test@example.com",
        role=UserRole.RESEARCHER,
        created_at=datetime.now(),
        last_access=datetime.now()
    )

    assert user.id == "user_id"
    assert user.username == "test_user"
    assert user.email == "test@example.com"
    assert user.role == UserRole.RESEARCHER


def test_user_username_validation():
    """Test validation of username."""
    with pytest.raises(ValueError):
        User(
            id="user_id",
            username="ab",  # Too short
            email="test@example.com",
            role=UserRole.RESEARCHER,
            created_at=datetime.now(),
        )


def test_user_email_validation():
    """Test validation of email."""
    with pytest.raises(ValueError):
        User(
            id="user_id",
            username="test_user",
            email="invalid_email",  # Invalid email format
            role=UserRole.RESEARCHER,
            created_at=datetime.now(),
        )


def test_user_role_enum_values():
    """Test that UserRole enum values are correct."""
    all_roles = [role.value for role in UserRole]
    expected_roles = ["researcher", "clinician", "legal_professional", "admin"]
    assert all(role in all_roles for role in expected_roles)


def test_user_role_validation():
    """Test role validation."""
    # Valid role should pass
    user = User(
        id="user_id",
        username="test_user",
        email="test@example.com",
        role=UserRole.CLINICIAN,  # Valid role
        created_at=datetime.now(),
    )
    assert user.role == UserRole.CLINICIAN