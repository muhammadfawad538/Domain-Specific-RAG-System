import pytest
from datetime import datetime
from src.models.query import Query, QueryDomain, QueryStatus


def test_query_creation():
    """Test successful creation of a Query object."""
    query = Query(
        id="test_id",
        content="What is the treatment for diabetes?",
        domain=QueryDomain.MEDICAL,
        user_id="user123",
        timestamp=datetime.now(),
        status=QueryStatus.PENDING
    )

    assert query.id == "test_id"
    assert query.content == "What is the treatment for diabetes?"
    assert query.domain == QueryDomain.MEDICAL
    assert query.user_id == "user123"
    assert query.status == QueryStatus.PENDING


def test_query_content_validation():
    """Test validation of query content."""
    with pytest.raises(ValueError):
        Query(
            id="test_id",
            content="",  # Empty content should fail
            domain=QueryDomain.MEDICAL,
            user_id="user_id",
        )


def test_query_domain_enum_values():
    """Test that QueryDomain enum values are correct."""
    assert QueryDomain.MEDICAL.value == "medical"
    assert QueryDomain.LEGAL.value == "legal"
    assert QueryDomain.UNKNOWN.value == "unknown"


def test_query_status_enum_values():
    """Test that QueryStatus enum values are correct."""
    assert QueryStatus.PENDING.value == "pending"
    assert QueryStatus.PROCESSING.value == "processing"
    assert QueryStatus.COMPLETED.value == "completed"
    assert QueryStatus.REJECTED.value == "rejected"