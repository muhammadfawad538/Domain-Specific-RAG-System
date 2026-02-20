---
title: Domain-Specific RAG System
emoji: 🤖
colorFrom: blue
colorTo: yellow
sdk: docker
app_file: app.py
pinned: false
---

# Domain-Specific Retrieval-Augmented Generation System

A domain-restricted Retrieval-Augmented Generation (RAG) system designed for medical and legal research that answers queries using only verified and curated documents while providing precise, traceable citations.

## Features

- **Evidence-First**: All generated content originates from retrieved documents
- **Citation Required**: All answers include source attribution
- **Domain Restricted**: Responses rely only on curated medical or legal sources
- **Safety Over Completeness**: Responds with "Insufficient verified evidence available" when appropriate
- **Agent-Governed Validation**: Multi-stage validation pipeline with independent agents
- **Data Source Authority**: Only approved sources are allowed

## Architecture

The system follows an agent-controlled RAG pipeline with these stages:

1. **Query Classification**: Identifies if the query is medical or legal
2. **Retrieval Investigation**: Fetches relevant document passages
3. **Evidence Validation**: Checks the quality of retrieved content
4. **Answer Generation**: Creates responses from validated sources
5. **Citation Audit**: Ensures proper attribution to sources
6. **Safety Review**: Applies safety controls and disclaimers

Each stage must be independently verifiable to ensure the integrity of the system.

## Prerequisites

- Python 3.9+
- pip package manager
- Access to an LLM API (OpenAI, Anthropic, or similar)

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
   python -m src.api.main
   ```

2. **Upload documents**
   Use the `/api/upload` endpoint to upload medical or legal documents

3. **Query the system**
   Use the `/api/query` endpoint to submit medical or legal questions

## API Endpoints

- `POST /api/query`: Submit a query and receive evidence-backed response with citations
- `POST /api/upload`: Upload documents for the knowledge base
- `GET /api/health`: Check system health status

## Key Components

- **Query Classifier**: Identifies whether the query is medical or legal
- **Retrieval Investigator**: Finds relevant document chunks based on the query
- **Evidence Validator**: Checks the quality and relevance of retrieved chunks
- **Citation Auditor**: Ensures all claims in responses are properly linked to sources
- **Safety Reviewer**: Applies safety controls and adds necessary disclaimers

## Data Model

The system uses these core entities:

- **Query**: Natural language questions from users
- **Document**: Vetted source files with medical/legal information
- **Chunk**: Semantic passages extracted from documents
- **Response**: System-generated answers with proper citations
- **Citation**: References linking claims to source documents
- **User**: System users with role-based access

## Development

To run tests:
```bash
pytest tests/
```

## Security and Compliance

This system is designed to handle sensitive medical and legal information with the following safeguards:

- All content is sourced from verified documents only
- Citations are required for all claims
- Safety disclaimers are automatically added to responses
- Insufficient evidence responses are provided when appropriate

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Deployment

### Hugging Face Spaces Deployment

This project includes automated deployment to Hugging Face Spaces via GitHub Actions. The workflow is triggered automatically when changes are pushed to the main branch.

To set up the deployment:

1. Create a Hugging Face account and a Space (either Docker-based or other runtime)
2. Obtain your Hugging Face access token from your account settings
3. Add these secrets to your GitHub repository:
   - `HF_TOKEN`: Your Hugging Face access token
   - `HF_REPO_ID`: Your Space repository ID (format: `username/space-name`)

The deployment workflow is defined in `.github/workflows/deploy-to-hf-spaces.yml` and will automatically sync your code to Hugging Face Spaces on each push to main.

### Manual Deployment

If you prefer to deploy manually, you can:

1. Create a Space on Hugging Face
2. Clone your Space repository locally
3. Copy the project files to the Space repository
4. Update the Space configuration as needed
5. Push the changes to Hugging Face

## Notes

This system is intended for research assistance and should not be used as professional medical or legal advice. Always consult with qualified professionals for medical or legal decisions.