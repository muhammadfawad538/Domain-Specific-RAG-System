import pytest
from datetime import datetime
from src.models.chunk import Chunk


def test_chunk_creation():
    """Test successful creation of a Chunk object."""
    chunk = Chunk(
        id="chunk_id",
        document_id="doc_id",
        content="This is the chunk content",
        chunk_index=0,
        embedding=[0.1, 0.2, 0.3],
        created_at=datetime.now()
    )

    assert chunk.id == "chunk_id"
    assert chunk.document_id == "doc_id"
    assert chunk.content == "This is the chunk content"
    assert chunk.chunk_index == 0
    assert chunk.embedding == [0.1, 0.2, 0.3]


def test_chunk_content_validation():
    """Test validation of chunk content."""
    with pytest.raises(ValueError):
        Chunk(
            id="chunk_id",
            document_id="doc_id",
            content="",  # Empty content should fail
            chunk_index=0,
            created_at=datetime.now()
        )


def test_chunk_index_validation():
    """Test validation of chunk index."""
    # Valid index should pass
    chunk = Chunk(
        id="chunk_id",
        document_id="doc_id",
        content="Valid content",
        chunk_index=5,  # Valid index
        created_at=datetime.now()
    )
    assert chunk.chunk_index == 5

    # Negative index should fail
    with pytest.raises(ValueError):
        Chunk(
            id="chunk_id",
            document_id="doc_id",
            content="Valid content",
            chunk_index=-1,  # Invalid index
            created_at=datetime.now()
        )


def test_chunk_embedding_validation():
    """Test validation of chunk embedding."""
    # Valid embedding should pass
    chunk = Chunk(
        id="chunk_id",
        document_id="doc_id",
        content="Valid content",
        chunk_index=0,
        embedding=[0.1, 0.2, 0.3],  # Valid embedding
        created_at=datetime.now()
    )
    assert chunk.embedding == [0.1, 0.2, 0.3]

    # Empty embedding should fail
    with pytest.raises(ValueError):
        Chunk(
            id="chunk_id",
            document_id="doc_id",
            content="Valid content",
            chunk_index=0,
            embedding=[],  # Empty embedding should fail
            created_at=datetime.now()
        )