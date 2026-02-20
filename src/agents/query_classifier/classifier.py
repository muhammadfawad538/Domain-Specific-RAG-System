from typing import Dict, Any
import asyncio
from src.models.query import Query, QueryDomain
from src.services.llm_service import LLMService
from src.utils.logger import setup_logger, log_agent_action

logger = setup_logger("agent.query_classifier")

class QueryClassifierAgent:
    """
    Agent responsible for identifying whether a query is medical or legal in nature.
    """

    def __init__(self, llm_service: LLMService):
        """
        Initialize the Query Classifier agent.

        Args:
            llm_service: The LLM service to use for classification
        """
        self.llm_service = llm_service

    async def process(self, query: Query) -> Query:
        """
        Process a query to classify its domain (medical or legal).

        Args:
            query: The query to classify

        Returns:
            The query object with updated domain classification
        """
        log_agent_action("query_classifier", "classification_started", {"query_id": query.id, "original_domain": str(query.domain)})

        try:
            # If domain was already specified, just confirm and return
            # With use_enum_values=True, query.domain is converted to string value
            if query.domain != "unknown":
                log_agent_action("query_classifier", "domain_already_known", {"query_id": query.id, "domain": query.domain})
                # Return the query as-is since domain is already set
                return Query(
                    id=query.id,
                    content=query.content,
                    domain=query.domain,
                    user_id=query.user_id,
                    timestamp=query.timestamp,
                    status=query.status
                )

            # Define classification prompt
            prompt = f"""
            Please classify the following query as either 'medical' or 'legal'. Respond with just one word: medical or legal.

            Query: {query.content}

            Classification:
            """

            # Use LLM to classify the query
            response = self.llm_service.generate_response(prompt)

            # Extract domain from response
            response_lower = response.lower().strip()
            if "medical" in response_lower or "health" in response_lower or "clinical" in response_lower:
                classified_domain = QueryDomain.MEDICAL
            elif "legal" in response_lower or "law" in response_lower or "court" in response_lower or "statute" in response_lower:
                classified_domain = QueryDomain.LEGAL
            else:
                # If uncertain, default to unknown
                classified_domain = QueryDomain.UNKNOWN

            # Update query with classification
            # With use_enum_values=True, the domain will be converted to string
            updated_query = Query(
                id=query.id,
                content=query.content,
                domain=classified_domain,
                user_id=query.user_id,
                timestamp=query.timestamp,
                status=query.status
            )

            log_agent_action("query_classifier", "classification_completed", {
                "query_id": query.id,
                "original_query": query.content[:100] + "..." if len(query.content) > 100 else query.content,
                "classified_domain": str(classified_domain)
            })

            return updated_query

        except Exception as e:
            logger.error(f"Error in query classification: {e}")
            log_agent_action("query_classifier", "classification_failed", {"query_id": query.id, "error": str(e)})

            # Return original query if classification fails
            return query

    def classify_by_keywords(self, query_text: str) -> QueryDomain:
        """
        Fallback method to classify query based on keywords.

        Args:
            query_text: The query text to classify

        Returns:
            The classified domain
        """
        query_lower = query_text.lower()

        # Medical keywords
        medical_keywords = [
            "patient", "treatment", "diagnosis", "disease", "symptom", "medication", "drug",
            "therapy", "surgery", "hospital", "doctor", "clinical", "medical", "health",
            "prescription", "condition", "illness", "therapy", "medicine", "treatment"
        ]

        # Legal keywords
        legal_keywords = [
            "court", "law", "legal", "case", "statute", "regulation", "contract", "agreement",
            "attorney", "lawyer", "litigation", "judgment", "ruling", "precedent", "liability",
            "compliance", "regulatory", "doctrine", "jurisdiction", "counsel", "brief"
        ]

        medical_count = sum(1 for keyword in medical_keywords if keyword in query_lower)
        legal_count = sum(1 for keyword in legal_keywords if keyword in query_lower)

        if medical_count > legal_count:
            return QueryDomain.MEDICAL
        elif legal_count > medical_count:
            return QueryDomain.LEGAL
        else:
            return QueryDomain.UNKNOWN