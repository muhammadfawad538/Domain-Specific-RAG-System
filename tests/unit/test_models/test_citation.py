import pytest
from datetime import datetime
from src.models.citation import Citation


def test_citation_creation():
    """Test successful creation of a Citation object."""
    citation = Citation(
        id="citation_id",
        response_id="response_id",
        chunk_id="chunk_id",
        document_id="document_id",
        claim_text="This is the claim text",
        citation_text="This is the citation text",
        document_title="Document Title",
        confidence=0.9,
        created_at=datetime.now()
    )

    assert citation.id == "citation_id"
    assert citation.response_id == "response_id"
    assert citation.chunk_id == "chunk_id"
    assert citation.document_id == "document_id"
    assert citation.claim_text == "This is the claim text"
    assert citation.citation_text == "This is the citation text"
    assert citation.document_title == "Document Title"
    assert citation.confidence == 0.9


def test_citation_text_validation():
    """Test validation of citation text fields."""
    with pytest.raises(ValueError):
        Citation(
            id="citation_id",
            response_id="response_id",
            chunk_id="chunk_id",
            document_id="document_id",
            claim_text="",  # Empty text should fail
            citation_text="Valid citation text",
            created_at=datetime.now()
        )

    with pytest.raises(ValueError):
        Citation(
            id="citation_id",
            response_id="response_id",
            chunk_id="chunk_id",
            document_id="document_id",
            claim_text="Valid claim text",
            citation_text="",  # Empty text should fail
            created_at=datetime.now()
        )


def test_citation_confidence_validation():
    """Test confidence value validation."""
    # Valid confidence value
    citation = Citation(
        id="citation_id",
        response_id="response_id",
        chunk_id="chunk_id",
        document_id="document_id",
        claim_text="Valid claim text",
        citation_text="Valid citation text",
        confidence=0.8,
        created_at=datetime.now()
    )
    assert citation.confidence == 0.8

    # Invalid confidence value should raise error during validation
    with pytest.raises(ValueError):
        Citation(
            id="citation_id",
            response_id="response_id",
            chunk_id="chunk_id",
            document_id="document_id",
            claim_text="Valid claim text",
            citation_text="Valid citation text",
            confidence=1.5,  # Invalid value
            created_at=datetime.now()
        )