# Quickstart Guide: Domain-Specific Retrieval-Augmented Generation System

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Git
- Access to an LLM API (OpenAI, Anthropic, or similar)
- Local storage for document files

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   # or ANTHROPIC_API_KEY=your_anthropic_api_key_here

   # Vector database (FAISS path)
   VECTOR_DB_PATH=./data/vector_db

   # Document storage path
   DOCUMENT_STORAGE_PATH=./data/documents

   # Logging level
   LOG_LEVEL=INFO
   ```

## Running the System

1. **Initialize the system**
   ```bash
   python -m src.init_database
   ```

2. **Upload documents**
   ```bash
   python -m src.upload_documents --path /path/to/your/documents --domain medical
   ```

3. **Process documents into embeddings**
   ```bash
   python -m src.process_documents
   ```

4. **Start the query service**
   ```bash
   python -m src.query_service --port 8000
   ```

5. **Query the system**
   ```bash
   curl -X POST http://localhost:8000/query \
        -H "Content-Type: application/json" \
        -d '{"query": "What are the latest guidelines for diabetes treatment?", "user_id": "user123"}'
   ```

## Key Components

The system consists of several key components based on the agent architecture:

- **Query Classifier**: Identifies whether the query is medical or legal
- **Retrieval Investigator**: Finds relevant document chunks based on the query
- **Evidence Validator**: Checks the quality and relevance of retrieved chunks
- **Citation Auditor**: Ensures all claims in responses are properly linked to sources
- **Safety Reviewer**: Applies safety controls and adds necessary disclaimers

## API Endpoints

- `POST /query`: Submit a query and receive evidence-backed response
- `POST /upload`: Upload documents for the knowledge base
- `GET /documents`: List all documents in the knowledge base
- `GET /health`: Check system health status

## Development

To run tests:
```bash
pytest tests/
```

To run specific component tests:
```bash
pytest tests/test_query_classifier.py
pytest tests/test_retrieval_investigator.py
pytest tests/test_evidence_validator.py
pytest tests/test_citation_auditor.py
pytest tests/test_safety_reviewer.py
```