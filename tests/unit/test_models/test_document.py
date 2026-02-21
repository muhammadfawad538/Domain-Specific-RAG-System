import pytest
from datetime import datetime
from src.models.document import Document, DocumentDomain, FileFormat


def test_document_creation():
    """Test successful creation of a Document object."""
    document = Document(
        id="doc_id",
        title="Test Document",
        author="Test Author",
        publication="Test Publication",
        year=2023,
        file_path="/path/to/file",
        file_format=FileFormat.PDF,
        domain=DocumentDomain.MEDICAL,
        uploaded_by="user123",
        chunk_count=5
    )

    assert document.id == "doc_id"
    assert document.title == "Test Document"
    assert document.author == "Test Author"
    assert document.year == 2023
    assert document.file_format == FileFormat.PDF
    assert document.domain == DocumentDomain.MEDICAL
    assert document.chunk_count == 5


def test_document_title_validation():
    """Test validation of document title."""
    with pytest.raises(ValueError):
        Document(
            id="doc_id",
            title="",  # Empty title should fail
            author="Test Author",
            year=2023,
            file_path="/path/to/file",
            file_format=FileFormat.PDF,
            domain=DocumentDomain.MEDICAL,
            uploaded_by="user123",
        )


def test_document_year_validation():
    """Test validation of document year."""
    current_year = datetime.now().year

    # Valid year should pass
    doc = Document(
        id="doc_id",
        title="Test Document",
        author="Test Author",
        year=current_year,  # Current year should be valid
        file_path="/path/to/file",
        file_format=FileFormat.PDF,
        domain=DocumentDomain.MEDICAL,
        uploaded_by="user123",
    )
    assert doc.year == current_year

    # Invalid year should fail
    with pytest.raises(ValueError):
        Document(
            id="doc_id",
            title="Test Document",
            author="Test Author",
            year=1800,  # Too old year should fail
            file_path="/path/to/file",
            file_format=FileFormat.PDF,
            domain=DocumentDomain.MEDICAL,
            uploaded_by="user123",
        )


def test_document_format_validation():
    """Test document format validation."""
    # Valid format should pass
    doc = Document(
        id="doc_id",
        title="Test Document",
        author="Test Author",
        year=2023,
        file_path="/path/to/file",
        file_format=FileFormat.TEXT,  # Valid format
        domain=DocumentDomain.MEDICAL,
        uploaded_by="user123",
    )
    assert doc.file_format == FileFormat.TEXT


def test_document_domain_enum_values():
    """Test that DocumentDomain enum values are correct."""
    all_domains = [domain.value for domain in DocumentDomain]
    expected_domains = ["medical", "legal", "mixed"]
    assert all(domain in all_domains for domain in expected_domains)