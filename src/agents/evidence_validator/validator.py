from typing import List
import asyncio
from src.models.query import Query
from src.models.chunk import Chunk
from src.services.llm_service import LLMService
from src.utils.logger import setup_logger, log_agent_action

logger = setup_logger("agent.evidence_validator")

class EvidenceValidatorAgent:
    """
    Agent responsible for checking the quality and relevance of retrieved chunks.
    """

    def __init__(self, llm_service: LLMService):
        """
        Initialize the Evidence Validator agent.

        Args:
            llm_service: The LLM service to use for validation
        """
        self.llm_service = llm_service

    async def process(self, query: Query, retrieved_chunks: List[Chunk]) -> List[Chunk]:
        """
        Validate the quality and relevance of retrieved chunks.

        Args:
            query: The original query
            retrieved_chunks: List of chunks retrieved from the database

        Returns:
            List of validated (relevant and high-quality) chunks
        """
        log_agent_action("evidence_validator", "validation_started", {
            "query_id": query.id,
            "chunks_to_validate": len(retrieved_chunks),
            "query_domain": query.domain
        })

        try:
            validated_chunks = []
            for chunk in retrieved_chunks:
                is_valid = await self.validate_chunk(query, chunk)
                if is_valid:
                    validated_chunks.append(chunk)

            log_agent_action("evidence_validator", "validation_completed", {
                "query_id": query.id,
                "chunks_validated": len(retrieved_chunks),
                "chunks_approved": len(validated_chunks),
                "validation_rate": f"{len(validated_chunks)/len(retrieved_chunks)*100:.1f}%" if retrieved_chunks else "0%"
            })

            return validated_chunks

        except Exception as e:
            logger.error(f"Error in evidence validation: {e}")
            log_agent_action("evidence_validator", "validation_failed", {"query_id": query.id, "error": str(e)})

            # Return original chunks if validation fails
            return retrieved_chunks

    async def validate_chunk(self, query: Query, chunk: Chunk) -> bool:
        """
        Validate a single chunk against the query.

        Args:
            query: The original query
            chunk: The chunk to validate

        Returns:
            True if the chunk is valid and relevant, False otherwise
        """
        try:
            # Create a validation prompt for the LLM
            prompt = f"""
            Determine if the following text chunk is relevant and contains reliable evidence to answer the query.
            Consider the domain of the query when evaluating reliability.

            Query: {query.content}
            Query Domain: {query.domain}

            Text Chunk: {chunk.content}

            Please respond with ONLY 'RELEVANT' if the chunk is relevant and contains reliable information related to the query,
            or 'NOT_RELEVANT' if it is not relevant or does not contain reliable information.
            """

            response = self.llm_service.generate_response(prompt)

            # Check the response to determine if chunk is valid
            response_clean = response.strip().upper()
            is_relevant = "RELEVANT" in response_clean

            log_agent_action("evidence_validator", "chunk_evaluated", {
                "query_id": query.id,
                "chunk_id": chunk.id,
                "chunk_length": len(chunk.content),
                "is_relevant": is_relevant
            })

            return is_relevant

        except Exception as e:
            logger.error(f"Error validating chunk {chunk.id}: {e}")
            # Default to including the chunk if validation fails
            return True  # Be permissive in case of validation errors

    def validate_by_rules(self, query: Query, chunk: Chunk) -> bool:
        """
        Rule-based validation as a fallback or complement to LLM validation.

        Args:
            query: The original query
            chunk: The chunk to validate

        Returns:
            True if the chunk passes rule-based validation, False otherwise
        """
        try:
            query_lower = query.content.lower()
            chunk_lower = chunk.content.lower()

            # Basic checks
            # 1. Check if chunk is too short (less than 10 characters)
            if len(chunk.content.strip()) < 10:
                return False

            # 2. Check if query terms appear in chunk (simple keyword matching)
            query_words = query_lower.split()
            if not query_words:
                return True  # If query is empty, keep the chunk

            # Count how many query words appear in the chunk
            matching_words = [word for word in query_words if word in chunk_lower]
            match_ratio = len(matching_words) / len(query_words)

            # Consider it relevant if at least 30% of query words are present
            # Or if at least one important word is present
            if match_ratio >= 0.3:
                return True

            # 3. Additional domain-specific validation could go here
            # For example, checking if medical chunks contain medical terminology
            # when the query is medical

            return False

        except Exception as e:
            logger.error(f"Error in rule-based validation for chunk {chunk.id}: {e}")
            return False