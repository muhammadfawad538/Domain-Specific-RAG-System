import asyncio
from typing import List
from src.models.chunk import Chunk
from src.services.llm_service import get_llm_service
from src.utils.logger import setup_logger

logger = setup_logger("embedding_service")

class EmbeddingService:
    """
    Service for generating embeddings for text chunks using LLM service.
    """

    def __init__(self):
        self.llm_service = get_llm_service()

    async def generate_embeddings(self, chunks: List[Chunk]) -> List[List[float]]:
        """
        Generate embeddings for a list of chunks.

        Args:
            chunks: List of Chunk objects to generate embeddings for

        Returns:
            List of embedding vectors corresponding to the input chunks
        """
        try:
            logger.info(f"Generating embeddings for {len(chunks)} chunks")

            embeddings = []
            for i, chunk in enumerate(chunks):
                # Generate embedding for the chunk content
                embedding = self.llm_service.embed_text(chunk.content)
                embeddings.append(embedding)

                # Log progress every 10 chunks
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(chunks)} chunks for embedding")

            logger.info(f"Successfully generated embeddings for {len(chunks)} chunks")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    async def generate_embedding_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text strings in batch mode.

        Args:
            texts: List of text strings to generate embeddings for

        Returns:
            List of embedding vectors corresponding to the input texts
        """
        logger.info(f"Generating embeddings for {len(texts)} text items in batch mode")

        # For now, process sequentially
        # In a real implementation, this might use batch API calls if supported by the LLM service
        embeddings = []
        for i, text in enumerate(texts):
            try:
                embedding = self.llm_service.embed_text(text)
                embeddings.append(embedding)

                # Log progress every 10 items
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(texts)} text items for embedding")
            except Exception as e:
                logger.error(f"Error generating embedding for text item {i}: {e}")
                # Add a zero vector as placeholder, or handle differently based on requirements
                embeddings.append([0.0] * 1536)  # Assuming 1536-dim embeddings like OpenAI

        logger.info(f"Completed embedding generation for {len(texts)} text items")
        return embeddings

    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Cosine similarity score between -1 and 1
        """
        try:
            import numpy as np

            # Convert to numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)

            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0

    async def find_similar_chunks(self, query_embedding: List[float],
                                  chunks: List[Chunk],
                                  threshold: float = 0.7) -> List[Chunk]:
        """
        Find chunks similar to a query embedding based on a similarity threshold.

        Args:
            query_embedding: The embedding to compare against
            chunks: List of chunks to compare with
            threshold: Minimum similarity score to include a chunk

        Returns:
            List of chunks with similarity above the threshold
        """
        try:
            similar_chunks = []
            for chunk in chunks:
                if chunk.embedding is not None:
                    similarity = self.calculate_similarity(query_embedding, chunk.embedding)
                    if similarity >= threshold:
                        similar_chunks.append(chunk)
                else:
                    # If chunk doesn't have an embedding yet, skip it
                    continue

            logger.info(f"Found {len(similar_chunks)} similar chunks out of {len(chunks)}")
            return similar_chunks
        except Exception as e:
            logger.error(f"Error finding similar chunks: {e}")
            raise