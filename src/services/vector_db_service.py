import faiss
import numpy as np
import pickle
import os
from typing import List, Optional, Tuple
from src.models.chunk import Chunk
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("vector_db_service")

class VectorDBService:
    """
    Service for managing the FAISS vector database for document embeddings.
    """

    def __init__(self, index_path: Optional[str] = None):
        """
        Initialize the vector database service.

        Args:
            index_path: Path to load/save the FAISS index. If None, uses Config.VECTOR_DB_PATH
        """
        self.index_path = index_path or Config.VECTOR_DB_PATH
        self.index_file = os.path.join(self.index_path, "faiss.index")
        self.metadata_file = os.path.join(self.index_path, "metadata.pkl")

        # Ensure directory exists
        os.makedirs(self.index_path, exist_ok=True)

        # Initialize the FAISS index
        self.dimension = 1536  # Default for OpenAI embeddings, will be adjusted as needed
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []  # Store metadata for each vector (chunk_id, document_id, etc.)

        # Load existing index if available
        self.load_index()

    def load_index(self):
        """Load the FAISS index and metadata from disk."""
        try:
            if os.path.exists(self.index_file):
                self.index = faiss.read_index(self.index_file)

            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)

            logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
        except Exception as e:
            logger.warning(f"Could not load existing index: {e}. Starting with empty index.")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    def save_index(self):
        """Save the FAISS index and metadata to disk."""
        try:
            # Update dimension based on current index if needed
            if self.index.ntotal > 0:
                self.dimension = self.index.d

            faiss.write_index(self.index, self.index_file)

            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)

            logger.info(f"Saved FAISS index with {self.index.ntotal} vectors")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise

    def add_embeddings(self, chunks: List[Chunk], embeddings: List[List[float]]):
        """
        Add embeddings for chunks to the vector database.

        Args:
            chunks: List of Chunk objects
            embeddings: List of embedding vectors corresponding to the chunks
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")

        # Convert embeddings to numpy array
        embeddings_array = np.array(embeddings).astype('float32')

        # Adjust index dimension if necessary
        if self.index.d != embeddings_array.shape[1]:
            if self.index.ntotal == 0:
                # Create new index with correct dimension
                old_index = self.index
                self.dimension = embeddings_array.shape[1]
                self.index = faiss.IndexFlatL2(self.dimension)
                logger.info(f"Created new FAISS index with dimension {self.dimension}")
            else:
                raise ValueError(f"Embedding dimension mismatch: expected {self.index.d}, got {embeddings_array.shape[1]}")

        # Add embeddings to the index
        self.index.add(embeddings_array)

        # Add metadata for each chunk
        for chunk in chunks:
            self.metadata.append({
                'chunk_id': chunk.id,
                'document_id': chunk.document_id,
                'content': chunk.content,
                'chunk_index': chunk.chunk_index
            })

        logger.info(f"Added {len(chunks)} embeddings to index. Total: {self.index.ntotal}")

    def search(self, query_embedding: List[float], k: int = 5) -> List[Tuple[Chunk, float]]:
        """
        Search for similar chunks to the query embedding.

        Args:
            query_embedding: The embedding vector to search for
            k: Number of results to return

        Returns:
            List of tuples containing (Chunk, distance) sorted by distance
        """
        if self.index.ntotal == 0:
            return []

        # Convert query embedding to numpy array
        query_array = np.array([query_embedding]).astype('float32')

        # Perform search
        distances, indices = self.index.search(query_array, k)

        # Format results
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                metadata = self.metadata[idx]
                # Create a minimal Chunk object with the metadata
                chunk = Chunk(
                    id=metadata['chunk_id'],
                    document_id=metadata['document_id'],
                    content=metadata['content'],
                    chunk_index=metadata['chunk_index'],
                    embedding=None  # Don't include the full embedding in the result
                )
                results.append((chunk, float(dist)))

        logger.info(f"Search returned {len(results)} results")
        return results

    def get_chunk_by_id(self, chunk_id: str) -> Optional[Chunk]:
        """
        Retrieve a chunk by its ID.

        Args:
            chunk_id: The ID of the chunk to retrieve

        Returns:
            The Chunk object if found, None otherwise
        """
        for i, metadata in enumerate(self.metadata):
            if metadata['chunk_id'] == chunk_id:
                return Chunk(
                    id=metadata['chunk_id'],
                    document_id=metadata['document_id'],
                    content=metadata['content'],
                    chunk_index=metadata['chunk_index'],
                    embedding=None
                )
        return None

    def remove_document(self, document_id: str):
        """
        Remove all chunks associated with a document from the vector database.

        Args:
            document_id: The ID of the document to remove
        """
        # Find indices of chunks belonging to this document
        indices_to_remove = []
        for i, metadata in enumerate(self.metadata):
            if metadata['document_id'] == document_id:
                indices_to_remove.append(i)

        if not indices_to_remove:
            logger.info(f"No chunks found for document {document_id}")
            return

        # Remove from metadata (reverse order to maintain indices)
        indices_to_remove.reverse()
        for idx in indices_to_remove:
            self.metadata.pop(idx)

        # Recreate index without the removed vectors
        # This is a simple approach - in production, you might want a more efficient method
        if len(self.metadata) == 0:
            # If no metadata left, create a new empty index
            self.index = faiss.IndexFlatL2(self.dimension)
        else:
            # Extract remaining embeddings
            remaining_embeddings = []
            for metadata in self.metadata:
                # Note: This approach assumes we have a way to retrieve embeddings
                # In a real implementation, you'd need to store embeddings separately
                # For now, we'll just recreate an empty index
                pass

            # For now, just create a new empty index
            self.index = faiss.IndexFlatL2(self.dimension)
            # The embeddings would need to be re-added in a real implementation
            logger.info(f"Removed document {document_id} and its {len(indices_to_remove)} chunks")

    def get_stats(self) -> dict:
        """
        Get statistics about the vector database.

        Returns:
            Dictionary with statistics about the database
        """
        return {
            'total_vectors': self.index.ntotal,
            'dimension': self.index.d,
            'total_chunks': len(self.metadata)
        }