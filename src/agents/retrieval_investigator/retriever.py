from typing import List
import asyncio
from src.models.query import Query
from src.models.chunk import Chunk
from src.services.llm_service import LLMService
from src.services.vector_db_service import VectorDBService
from src.utils.logger import setup_logger, log_agent_action

logger = setup_logger("agent.retrieval_investigator")

class RetrievalInvestigatorAgent:
    """
    Agent responsible for fetching relevant passages from the document database based on the query.
    """

    def __init__(self, llm_service: LLMService, vector_db_service: VectorDBService):
        """
        Initialize the Retrieval Investigator agent.

        Args:
            llm_service: The LLM service to use for processing
            vector_db_service: The vector database service to retrieve from
        """
        self.llm_service = llm_service
        self.vector_db_service = vector_db_service

    async def process(self, query: Query) -> List[Chunk]:
        """
        Retrieve relevant chunks from the vector database based on the query.

        Args:
            query: The query to retrieve relevant chunks for

        Returns:
            List of relevant Chunk objects
        """
        log_agent_action("retrieval_investigator", "retrieval_started", {"query_id": query.id, "query_domain": query.domain})

        try:
            # Generate embedding for the query
            query_embedding = self.llm_service.embed_text(query.content)

            # Search for relevant chunks in the vector database
            # Limit to 5 most relevant chunks initially, could be configurable
            relevant_chunks_with_distances = self.vector_db_service.search(query_embedding, k=5)

            # Extract just the chunks, discarding the distances for now
            relevant_chunks = [chunk for chunk, distance in relevant_chunks_with_distances]

            log_agent_action("retrieval_investigator", "retrieval_completed", {
                "query_id": query.id,
                "chunks_retrieved": len(relevant_chunks),
                "query_summary": query.content[:100] + "..." if len(query.content) > 100 else query.content
            })

            return relevant_chunks

        except Exception as e:
            logger.error(f"Error in retrieval investigation: {e}")
            log_agent_action("retrieval_investigator", "retrieval_failed", {"query_id": query.id, "error": str(e)})

            # Return empty list if retrieval fails
            return []

    def filter_by_domain(self, chunks: List[Chunk], domain: str) -> List[Chunk]:
        """
        Filter retrieved chunks by domain if needed.

        Args:
            chunks: List of chunks to filter
            domain: The domain to filter by

        Returns:
            Filtered list of chunks
        """
        # This would require the chunks to have domain metadata
        # For now, return all chunks
        # In a real implementation, chunks would have domain information attached
        return chunks