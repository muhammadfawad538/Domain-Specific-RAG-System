from typing import List
import asyncio
from src.models.query import Query
from src.models.response import Response
from src.models.chunk import Chunk
from src.models.citation import Citation
from src.services.llm_service import LLMService
from src.utils.logger import setup_logger, log_agent_action

logger = setup_logger("agent.citation_auditor")

class CitationAuditorAgent:
    """
    Agent responsible for ensuring all claims in responses are properly linked to source documents.
    """

    def __init__(self, llm_service: LLMService):
        """
        Initialize the Citation Auditor agent.

        Args:
            llm_service: The LLM service to use for citation auditing
        """
        self.llm_service = llm_service

    async def process(self, query: Query, response: Response, chunks: List[Chunk]) -> Response:
        """
        Audit the response to ensure all claims are properly cited.

        Args:
            query: The original query
            response: The generated response to audit
            chunks: The chunks used to generate the response

        Returns:
            The response object with citations added
        """
        log_agent_action("citation_auditor", "citation_audit_started", {
            "response_id": response.id,
            "query_id": query.id,
            "response_length": len(response.content),
            "available_chunks": len(chunks)
        })

        try:
            # Identify claims in the response that need citations
            claims_with_sources = await self.identify_claims_and_sources(response, chunks)

            # Create citations for each claim
            citations = []
            for claim, source_chunk in claims_with_sources:
                citation = Citation(
                    id=f"cite_{response.id}_{len(citations)+1}",
                    response_id=response.id,
                    chunk_id=source_chunk.id,
                    document_id=source_chunk.document_id,
                    claim_text=claim,
                    citation_text=source_chunk.content[:200] + "..." if len(source_chunk.content) > 200 else source_chunk.content,
                    document_title=getattr(source_chunk, 'title', f"Document {source_chunk.document_id}"),  # Would need to get from document metadata
                    confidence=0.9,  # Default confidence, would be calculated based on match quality
                )
                citations.append(citation)

            # Update the response with the citations
            audited_response = Response(
                id=response.id,
                query_id=response.query_id,
                content=response.content,
                status=response.status,
                citations=citations,
                created_at=response.created_at,
                confidence=response.confidence,
                disclaimers=response.disclaimers
            )

            log_agent_action("citation_auditor", "citation_audit_completed", {
                "response_id": response.id,
                "citations_added": len(citations),
                "query_id": query.id
            })

            return audited_response

        except Exception as e:
            logger.error(f"Error in citation auditing: {e}")
            log_agent_action("citation_auditor", "citation_audit_failed", {
                "response_id": response.id,
                "query_id": query.id,
                "error": str(e)
            })

            # Return original response if auditing fails
            return response

    async def identify_claims_and_sources(self, response: Response, chunks: List[Chunk]) -> List[tuple]:
        """
        Identify claims in the response and match them to source chunks.

        Args:
            response: The response to analyze
            chunks: The chunks that were used to generate the response

        Returns:
            List of tuples containing (claim_text, source_chunk)
        """
        try:
            # Create a prompt to identify claims in the response
            prompt = f"""
            Identify specific factual claims made in the following response that should be cited.
            For each claim, indicate which source chunk it came from based on similarity of content.

            Response: {response.content}

            Available source chunks:
            """

            for i, chunk in enumerate(chunks):
                prompt += f"\nChunk {i+1}: {chunk.content[:200]}{'...' if len(chunk.content) > 200 else ''}\n"

            prompt += "\nPlease identify claims from the response and match each to the most likely source chunk. List them as: CLAIM - SOURCE CHUNK ID"

            # Get LLM to identify claims and match them to sources
            result = self.llm_service.generate_response(prompt)

            # Parse the result to extract claims and their corresponding chunks
            # This is a simplified parsing - a real implementation would need more robust parsing
            claims_with_sources = []

            # Look for patterns like "CLAIM - SOURCE CHUNK ID" or similar formats
            lines = result.split('\n')
            for line in lines:
                if '-' in line and 'chunk' in line.lower():
                    # Simple parsing - in practice, this would need more robust NLP
                    parts = line.split('-')
                    if len(parts) >= 2:
                        claim = parts[0].strip()
                        source_identifier = parts[1].strip()

                        # Try to match the source identifier to one of our chunks
                        matched_chunk = None
                        for chunk in chunks:
                            # Simple matching - look for ID or content match
                            if source_identifier.lower() in chunk.id.lower() or source_identifier.lower() in chunk.content.lower():
                                matched_chunk = chunk
                                break

                        if matched_chunk:
                            claims_with_sources.append((claim, matched_chunk))

            # If LLM parsing didn't work well, fall back to a simpler approach
            if not claims_with_sources and chunks:
                # Simply link the response content to the most relevant chunk
                # (the first one for simplicity)
                if chunks:
                    claims_with_sources.append((response.content[:100] + "...", chunks[0]))

            log_agent_action("citation_auditor", "claims_identified", {
                "response_id": response.id,
                "claims_count": len(claims_with_sources)
            })

            return claims_with_sources

        except Exception as e:
            logger.error(f"Error identifying claims and sources: {e}")
            # Return a simple mapping if detailed analysis fails
            if chunks:
                return [(response.content[:100] + "...", chunks[0])]
            else:
                return []

    def validate_citation_accuracy(self, claim: str, source: str) -> float:
        """
        Validate how accurately a claim matches the source text.

        Args:
            claim: The claim made in the response
            source: The source text to validate against

        Returns:
            A confidence score between 0 and 1
        """
        try:
            # This would typically involve more sophisticated text similarity comparison
            # For now, we'll use a simple approach
            claim_lower = claim.lower()
            source_lower = source.lower()

            # Check if key terms from the claim appear in the source
            claim_words = set(claim_lower.split()[:10])  # Check first 10 words
            source_words = set(source_lower.split())

            if not claim_words:
                return 0.0

            matching_words = claim_words.intersection(source_words)
            accuracy_score = len(matching_words) / len(claim_words)

            # Cap the score to be between 0 and 1
            return min(1.0, max(0.0, accuracy_score))

        except Exception as e:
            logger.error(f"Error validating citation accuracy: {e}")
            return 0.0