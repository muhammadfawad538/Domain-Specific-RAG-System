import pytest
import os
import tempfile
from unittest.mock import Mock, patch
from src.services.vector_db_service import VectorDBService
from src.models.chunk import Chunk


def test_vector_db_service_initialization():
    """Test initialization of VectorDBService."""
    with tempfile.TemporaryDirectory() as temp_dir:
        service = VectorDBService(index_path=temp_dir)

        assert service.index_path == temp_dir
        assert service.index is not None  # Should have a FAISS index
        assert service.metadata == []  # Should start with empty metadata


def test_add_embeddings():
    """Test adding embeddings to the vector database."""
    with tempfile.TemporaryDirectory() as temp_dir:
        service = VectorDBService(index_path=temp_dir)

        # Create test chunks
        chunks = [
            Chunk(
                id="chunk1",
                document_id="doc1",
                content="Test content 1",
                chunk_index=0
            ),
            Chunk(
                id="chunk2",
                document_id="doc2",
                content="Test content 2",
                chunk_index=0
            )
        ]

        # Create test embeddings
        embeddings = [
            [0.1, 0.2, 0.3, 0.4],
            [0.5, 0.6, 0.7, 0.8]
        ]

        # Add embeddings
        service.add_embeddings(chunks, embeddings)

        # Check that embeddings were added
        assert service.index.ntotal == 2
        assert len(service.metadata) == 2
        assert service.metadata[0]['chunk_id'] == 'chunk1'
        assert service.metadata[1]['chunk_id'] == 'chunk2'


def test_get_stats():
    """Test getting statistics from the vector database."""
    with tempfile.TemporaryDirectory() as temp_dir:
        service = VectorDBService(index_path=temp_dir)

        # Initially should have 0 vectors
        stats = service.get_stats()
        assert stats['total_vectors'] == 0
        assert stats['total_chunks'] == 0

        # Add some embeddings
        chunks = [Chunk(id="chunk1", document_id="doc1", content="Test", chunk_index=0)]
        embeddings = [[0.1, 0.2, 0.3, 0.4]]
        service.add_embeddings(chunks, embeddings)

        # Now should have 1 vector
        stats = service.get_stats()
        assert stats['total_vectors'] == 1
        assert stats['total_chunks'] == 1


def test_get_chunk_by_id():
    """Test retrieving a chunk by its ID."""
    with tempfile.TemporaryDirectory() as temp_dir:
        service = VectorDBService(index_path=temp_dir)

        # Add a chunk
        chunks = [Chunk(id="chunk1", document_id="doc1", content="Test content", chunk_index=0)]
        embeddings = [[0.1, 0.2, 0.3, 0.4]]
        service.add_embeddings(chunks, embeddings)

        # Retrieve the chunk
        retrieved_chunk = service.get_chunk_by_id("chunk1")

        assert retrieved_chunk is not None
        assert retrieved_chunk.id == "chunk1"
        assert retrieved_chunk.document_id == "doc1"
        assert retrieved_chunk.content == "Test content"
        assert retrieved_chunk.chunk_index == 0
        assert retrieved_chunk.embedding is None  # Should not include embedding in result


def test_get_chunk_by_id_not_found():
    """Test retrieving a chunk that doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        service = VectorDBService(index_path=temp_dir)

        # Try to retrieve a chunk that doesn't exist
        retrieved_chunk = service.get_chunk_by_id("nonexistent")

        assert retrieved_chunk is None