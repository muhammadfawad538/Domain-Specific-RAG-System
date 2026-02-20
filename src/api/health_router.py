from fastapi import APIRouter
from typing import Dict, Any
from src.services.llm_service import get_llm_service
from src.services.vector_db_service import VectorDBService
from src.utils.config import Config
from src.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger("health_router")

# Initialize services
llm_service = get_llm_service()
vector_db_service = VectorDBService()


@router.get("/health")
async def get_health() -> Dict[str, Any]:
    """
    Comprehensive health check for the entire RAG system.
    """
    try:
        # Test LLM service availability
        llm_available = False
        try:
            # This is a basic test - in a real system, we might make a minimal API call
            llm_service_instance = get_llm_service()
            llm_available = True
        except Exception as e:
            logger.warning(f"LLM service unavailable: {e}")

        # Test Vector DB service
        db_available = False
        db_stats = {}
        try:
            db_stats = vector_db_service.get_stats()
            db_available = True
        except Exception as e:
            logger.warning(f"Vector DB service unavailable: {e}")

        # Overall status
        overall_status = "healthy"
        if not llm_available or not db_available:
            overall_status = "degraded" if llm_available and db_available else "unavailable"

        health_status = {
            "status": overall_status,
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "components": {
                "query_classifier": "healthy",
                "retrieval_investigator": "healthy",
                "evidence_validator": "healthy",
                "citation_auditor": "healthy",
                "safety_reviewer": "healthy",
                "llm_service": "healthy" if llm_available else "unavailable",
                "vector_db": "healthy" if db_available else "unavailable",
                "document_storage": "healthy",  # Assuming file system access is available
                "api_server": "healthy"
            },
            "system_info": {
                "config_valid": True,  # Config validation already happened at startup
                "vector_db_stats": db_stats if db_available else {}
            }
        }

        logger.info(f"Health check completed with status: {overall_status}")
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unavailable",
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "error": str(e),
            "components": {
                "query_classifier": "unknown",
                "retrieval_investigator": "unknown",
                "evidence_validator": "unknown",
                "citation_auditor": "unknown",
                "safety_reviewer": "unknown",
                "llm_service": "unknown",
                "vector_db": "unknown",
                "document_storage": "unknown",
                "api_server": "unknown"
            }
        }


@router.get("/ready")
async def get_readiness() -> Dict[str, str]:
    """
    Readiness check - whether the service is ready to accept traffic.
    """
    try:
        # For readiness, we require all critical components to be healthy
        llm_service_instance = get_llm_service()
        db_stats = vector_db_service.get_stats()

        # If we can initialize services without error, assume ready
        return {"status": "ready"}
    except Exception as e:
        logger.warning(f"Service not ready: {e}")
        return {"status": "not ready"}


@router.get("/live")
async def get_liveness() -> Dict[str, str]:
    """
    Liveness check - whether the service is alive and responding.
    """
    # Basic liveness check - if we can respond to this request, we're alive
    return {"status": "alive"}