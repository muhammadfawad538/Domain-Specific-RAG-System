# Starting the Domain-Specific RAG System Server

## Method 1: Manual Start (Recommended for Testing)

1. **Open a command prompt/terminal** in the project directory

2. **Install dependencies** (if not already done):
```bash
pip install -r requirements.txt
```

3. **Create a .env file** (even without API keys):
```bash
# Create an empty .env file to avoid warnings
echo "" > .env
```

4. **Start the server**:
```bash
python -m src.api.main
```

5. **The server will start on** `http://localhost:8000`

6. **Access the API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Method 2: Using Uvicorn Directly

1. **In the project directory, run**:
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing the Endpoints

Once the server is running, you can test the endpoints:

### Health Check (GET)
```bash
curl -X GET "http://localhost:8000/api/health"
```

### Query Processing (POST)
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What are the current medical guidelines for treating hypertension?",
    "user_id": "test_user_123",
    "domain": "UNKNOWN"
  }'
```

### Document Upload (POST) - Requires a PDF file
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  -F "title=Sample Document" \
  -F "domain=medical"
```

## Example Queries for Testing

### Medical Queries:
- "What are the current guidelines for diabetes management?"
- "Explain the treatment options for heart disease"
- "What are the symptoms of COVID-19?"

### Legal Queries:
- "What is the statute of limitations for contract disputes in California?"
- "Explain the legal requirements for business incorporation"
- "What are the rules for property transfer?"

## Notes for Testing without API Keys

The system will automatically use a **Mock LLM Service** when no API keys are provided, which:
- Simulates responses for testing purposes
- Provides mock citations
- Maintains the same interface as real LLM services
- Allows full system testing without external dependencies

## Troubleshooting

If you get errors about missing packages:
```bash
pip install "pydantic[email]"
pip install uvicorn
```

If you get import errors, make sure you're running from the project root directory (E:\Ass-2-it).