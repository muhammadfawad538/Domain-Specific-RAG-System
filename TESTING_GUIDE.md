# Testing Guide for Domain-Specific RAG System Endpoints

This guide shows how to test all the endpoints of the Domain-Specific Retrieval-Augmented Generation system without requiring API keys.

## Available Endpoints

### 1. Health Check Endpoints
- **GET /api/health** - Overall system health
- **GET /api/live** - Liveness check
- **GET /api/ready** - Readiness check

### 2. Query Processing Endpoint
- **POST /api/query** - Submit queries for processing

### 3. Document Management Endpoints
- **POST /api/upload** - Upload documents to the knowledge base

### 4. API Documentation
- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /redoc** - Alternative API documentation (ReDoc)

## Testing the System

### 1. Health Checks

```bash
# Check system health
curl -X GET "http://localhost:8000/api/health"

# Check liveness
curl -X GET "http://localhost:8000/api/live"

# Check readiness
curl -X GET "http://localhost:8000/api/ready"
```

### 2. Query Processing

#### Medical Queries
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the current medical guidelines for treating hypertension?",
    "user_id": "test_user_123"
  }'
```

#### Legal Queries
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the statute of limitations for medical malpractice in New York?",
    "user_id": "test_user_123"
  }'
```

#### Queries with Domain Specification
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the legal framework for property transfers",
    "user_id": "test_user_123",
    "domain": "legal"
  }'
```

### 3. API Documentation

Access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Mock Service Behavior

Since no API keys are provided, the system uses a **Mock LLM Service** that:
- Simulates responses for testing purposes
- Returns mock citations
- Maintains the same interface as real LLM services
- Allows full system testing without external dependencies

## Testing Script

You can also use the provided test script:

```bash
python test_endpoints.py
```

## Expected Response Format

Query responses follow this format:

```json
{
  "id": "response_id",
  "query_id": "query_id",
  "content": "Response content...",
  "status": "complete",
  "citations": [],
  "created_at": "2026-02-19T17:25:08.415011",
  "confidence": 0.8,
  "disclaimer": "This information is for research purposes only..."
}
```

## Troubleshooting

1. **Server not responding**: Make sure the server is running with `python -m src.api.main`

2. **Port already in use**: Change the port in the main.py file or stop other processes using port 8000

3. **Missing dependencies**: Install required packages with `pip install -r requirements.txt`

## Testing Without Starting Server

You can also test the mock service directly in Python:

```python
from src.services.llm_service import get_llm_service

# Get the mock service
service = get_llm_service()

# Test response generation
response = service.generate_response("Test query")
print(response)

# Test embedding generation
embedding = service.embed_text("Test text")
print(f"Embedding length: {len(embedding)}")
```

The system is now fully functional for testing purposes without requiring external API keys!