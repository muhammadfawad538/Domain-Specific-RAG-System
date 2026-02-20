from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from pydantic import BaseModel
from src.models.query import Query, QueryDomain
from src.models.response import Response, ResponseStatus
from src.models.citation import Citation
from src.agents.query_classifier.classifier import QueryClassifierAgent
from src.agents.retrieval_investigator.retriever import RetrievalInvestigatorAgent
from src.agents.evidence_validator.validator import EvidenceValidatorAgent
from src.agents.citation_auditor.auditor import CitationAuditorAgent
from src.agents.safety_reviewer.reviewer import SafetyReviewerAgent
from src.services.llm_service import get_llm_service
from src.services.vector_db_service import VectorDBService
from src.utils.logger import setup_logger, log_query_processing

router = APIRouter()
logger = setup_logger("query_router")

# Initialize services and agents
llm_service = get_llm_service()
vector_db_service = VectorDBService()

# Initialize agents with services
query_classifier = QueryClassifierAgent(llm_service)
retrieval_investigator = RetrievalInvestigatorAgent(llm_service, vector_db_service)
evidence_validator = EvidenceValidatorAgent(llm_service)
citation_auditor = CitationAuditorAgent(llm_service)
safety_reviewer = SafetyReviewerAgent(llm_service)

class QueryRequest(BaseModel):
    query: str
    user_id: str
    domain: QueryDomain = None

class QueryResponse(BaseModel):
    id: str
    query_id: str
    content: str
    status: ResponseStatus
    citations: List[Citation]
    created_at: str
    confidence: float = None
    disclaimer: str = None


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Submit a natural language query to the RAG system.
    """
    try:
        # Log the query processing start
        query_id = f"query_{hash(request.query) % 10000}"
        log_query_processing(query_id, request.user_id, "received", {"query_length": len(request.query)})

        # Create the query object
        query_obj = Query(
            id=query_id,
            content=request.query,
            domain=request.domain or QueryDomain.UNKNOWN,
            user_id=request.user_id,
            status="pending"
        )

        # Step 1: Query classification
        log_query_processing(query_id, request.user_id, "classifying")
        classified_query = await query_classifier.process(query_obj)
        log_query_processing(query_id, request.user_id, "classified", {"domain": classified_query.domain})

        # Step 2: Retrieval investigation
        log_query_processing(query_id, request.user_id, "retrieving")
        retrieved_chunks = await retrieval_investigator.process(classified_query)
        log_query_processing(query_id, request.user_id, "retrieved", {"chunks_count": len(retrieved_chunks)})

        # Step 3: Evidence validation
        log_query_processing(query_id, request.user_id, "validating")
        validated_chunks = await evidence_validator.process(classified_query, retrieved_chunks)
        log_query_processing(query_id, request.user_id, "validated", {"valid_chunks_count": len(validated_chunks)})

        # Step 4: Generate response using LLM
        log_query_processing(query_id, request.user_id, "generating_response")
        context_texts = [chunk.content for chunk in validated_chunks]
        response_content = llm_service.generate_response(classified_query.content, context_texts)

        # Create response object
        response_obj = Response(
            id=f"resp_{query_id}",
            query_id=query_id,
            content=response_content,
            status=ResponseStatus.COMPLETE if "insufficient verified evidence available" not in response_content.lower() else ResponseStatus.INSUFFICIENT_EVIDENCE,
            citations=[],
            confidence=0.8  # Default confidence, would be calculated based on various factors
        )

        # Step 5: Citation audit
        log_query_processing(query_id, request.user_id, "auditing_citations")
        audited_response = await citation_auditor.process(classified_query, response_obj, validated_chunks)
        log_query_processing(query_id, request.user_id, "citations_audited", {"citations_count": len(audited_response.citations)})

        # Step 6: Safety review
        log_query_processing(query_id, request.user_id, "safety_review")
        final_response = await safety_reviewer.process(audited_response)
        log_query_processing(query_id, request.user_id, "safety_review_completed")

        # Log completion
        log_query_processing(query_id, request.user_id, "completed", {"response_length": len(final_response.content)})

        # Format the response to match the expected API response model
        return QueryResponse(
            id=final_response.id,
            query_id=final_response.query_id,
            content=final_response.content,
            status=final_response.status,
            citations=final_response.citations,
            created_at=final_response.created_at.isoformat(),
            confidence=final_response.confidence,
            disclaimer=final_response.disclaimers
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        log_query_processing(query_id if 'query_id' in locals() else "unknown", request.user_id, "failed", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the query processing system.
    """
    try:
        # Check if LLM service is available
        llm_available = llm_service is not None

        # Check if vector DB service is available
        db_stats = vector_db_service.get_stats()

        health_status = {
            "status": "healthy" if llm_available else "degraded",
            "components": {
                "llm_service": "healthy" if llm_available else "unavailable",
                "vector_db": "healthy" if db_stats else "unavailable",
                "query_classifier": "initialized",
                "retrieval_investigator": "initialized",
                "evidence_validator": "initialized",
                "citation_auditor": "initialized",
                "safety_reviewer": "initialized"
            },
            "vector_db_stats": db_stats
        }

        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unavailable",
            "components": {
                "llm_service": "error",
                "vector_db": "error",
                "query_classifier": "error",
                "retrieval_investigator": "error",
                "evidence_validator": "error",
                "citation_auditor": "error",
                "safety_reviewer": "error"
            }
        }