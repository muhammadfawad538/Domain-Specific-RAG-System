import pytest
from datetime import datetime
from src.models.response import Response, ResponseStatus
from src.models.citation import Citation

def test_response_creation():
    """Test successful creation of a Response object."""
    response = Response(
        id="response_id",
        query_id="query_id",
        content="This is the response content",
        status=ResponseStatus.COMPLETE,
        citations=[],
        created_at=datetime.now(),
        confidence=0.85,
        disclaimers="This is a disclaimer"
    )

    assert response.id == "response_id"
    assert response.query_id == "query_id"
    assert response.content == "This is the response content"
    assert response.status == ResponseStatus.COMPLETE
    assert response.citations == []
    assert response.confidence == 0.85
    assert response.disclaimers == "This is a disclaimer"


def test_response_insufficient_evidence_validation():
    """Test validation when status is insufficient_evidence."""
    # This should pass: status is insufficient_evidence and content is empty
    response = Response(
        id="response_id",
        query_id="query_id",
        content="",
        status=ResponseStatus.INSUFFICIENT_EVIDENCE,
        citations=[],
        created_at=datetime.now(),
    )
    assert response.status == ResponseStatus.INSUFFICIENT_EVIDENCE


def test_response_status_enum_values():
    """Test that ResponseStatus enum values are correct."""
    assert ResponseStatus.COMPLETE.value == "complete"
    assert ResponseStatus.INSUFFICIENT_EVIDENCE.value == "insufficient_evidence"
    assert ResponseStatus.REJECTED.value == "rejected"


def test_response_confidence_validation():
    """Test confidence value validation."""
    # Valid confidence value
    response = Response(
        id="response_id",
        query_id="query_id",
        content="Content",
        status=ResponseStatus.COMPLETE,
        citations=[],
        created_at=datetime.now(),
        confidence=0.75
    )
    assert response.confidence == 0.75

    # Invalid confidence value should raise error during validation
    with pytest.raises(ValueError):
        Response(
            id="response_id",
            query_id="query_id",
            content="Content",
            status=ResponseStatus.COMPLETE,
            citations=[],
            created_at=datetime.now(),
            confidence=1.5  # Invalid value
        )