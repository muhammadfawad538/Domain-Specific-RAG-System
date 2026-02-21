---
id: 001
title: Domain Specific RAG Implementation
stage: general
date: 2026-02-19
surface: agent
model: claude-opus-4-6
feature: none
branch: master
user: FRIENDS PC
command: /sp.implement
labels: [rag, medical, legal, ai, implementation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - src/models/query.py
 - src/models/response.py
 - src/models/citation.py
 - src/models/user.py
 - src/models/document.py
 - src/models/chunk.py
 - src/agents/query_classifier/classifier.py
 - src/agents/retrieval_investigator/retriever.py
 - src/agents/evidence_validator/validator.py
 - src/agents/citation_auditor/auditor.py
 - src/agents/safety_reviewer/reviewer.py
 - src/services/vector_db_service.py
 - src/services/llm_service.py
 - src/services/document_processor.py
 - src/services/embedding_service.py
 - src/api/query_router.py
 - src/api/upload_router.py
 - src/utils/logger.py
 - src/config/settings.py
 - tests/unit/test_models/test_query.py
 - tests/unit/test_models/test_response.py
 - tests/unit/test_models/test_citation.py
 - tests/unit/test_models/test_user.py
 - tests/unit/test_models/test_document.py
 - tests/unit/test_models/test_chunk.py
 - tests/unit/test_agents/test_query_classifier.py
 - tests/unit/test_agents/test_retrieval_investigator.py
 - tests/unit/test_agents/test_evidence_validator.py
 - tests/unit/test_agents/test_citation_auditor.py
 - tests/unit/test_agents/test_safety_reviewer.py
 - tests/unit/test_services/test_vector_db_service.py
 - tests/unit/test_services/test_llm_service.py
 - tests/unit/test_services/test_document_processor.py
 - tests/unit/test_services/test_embedding_service.py
 - tests/unit/test_api/test_query_router.py
 - tests/unit/test_api/test_upload_router.py
 - tests/test_main.py
 - requirements.txt
 - setup.py
 - Dockerfile
 - docker-compose.yml
 - .gitignore
 - README.md
 - src/__init__.py
 - src/agents/__init__.py
 - src/agents/query_classifier/__init__.py
 - src/agents/retrieval_investigator/__init__.py
 - src/agents/evidence_validator/__init__.py
 - src/agents/citation_auditor/__init__.py
 - src/agents/safety_reviewer/__init__.py
 - src/api/__init__.py
 - src/services/__init__.py
 - src/utils/__init__.py
 - src/config/__init__.py
tests:
 - tests/unit/test_models/test_query.py
 - tests/unit/test_models/test_response.py
 - tests/unit/test_models/test_citation.py
 - tests/unit/test_models/test_user.py
 - tests/unit/test_models/test_document.py
 - tests/unit/test_models/test_chunk.py
 - tests/unit/test_agents/test_query_classifier.py
 - tests/unit/test_agents/test_retrieval_investigator.py
 - tests/unit/test_agents/test_evidence_validator.py
 - tests/unit/test_agents/test_citation_auditor.py
 - tests/unit/test_agents/test_safety_reviewer.py
 - tests/unit/test_services/test_vector_db_service.py
 - tests/unit/test_services/test_llm_service.py
 - tests/unit/test_services/test_document_processor.py
 - tests/unit/test_services/test_embedding_service.py
 - tests/unit/test_api/test_query_router.py
 - tests/unit/test_api/test_upload_router.py
 - tests/test_main.py
---

## Prompt

```
# /sp.specify — Project Specification

## Domain-Specific Retrieval-Augmented Generation for Medical and Legal Research

---

## 1. Project Goal

Build a **domain-restricted Retrieval-Augmented Generation (RAG) system** that answers medical and legal research queries using only verified and curated documents while providing precise, traceable citations.

The system aims to reduce hallucinations and improve trustworthiness in high-stakes knowledge domains.

---

## 2. Target Users

* Medical researchers
* Clinicians and healthcare professionals
* Legal researchers
* Lawyers and policy analysts
* Academic researchers and students

---

## 3. Core Problem

Current large language models:

* Generate confident but incorrect answers
* Lack strict source grounding
* Do not guarantee citation accuracy
* Mix verified and unverified knowledge

Users require a system that ensures:

* Evidence-backed responses
* Transparent citations
* Controlled knowledge sources
* Auditability of generated answers

---

## 4. Functional Requirements

### 4.1 Document Management

* Upload and store vetted medical or legal documents
* Support PDF and text formats
* Maintain document metadata (title, author, publication, year)

### 4.2 Data Processing

* Chunk documents into semantic passages
* Generate vector embeddings
* Store embeddings in a vector database (e.g., FAISS or Pinecone)

### 4.3 Query Processing

* Accept natural language queries
* Classify query domain (medical or legal)
* Retrieve top relevant passages

### 4.4 Answer Generation

* Generate answers ONLY from retrieved content
* Prevent unsupported knowledge generation
* Provide structured responses

### 4.5 Citation System

* Link each claim to source passages
* Display document name and section reference
* Prevent citation fabrication

### 4.6 Safety Controls

* Detect insufficient evidence
* Refuse unsupported queries
* Add safety disclaimers when required

---

## 5. Non-Functional Requirements

* High factual accuracy
* Low hallucination rate
* Fast retrieval response (< 3 seconds target)
* Scalable document indexing
* Transparent logging and audit trails

---

## 6. User Stories

### Researcher

> As a researcher, I want answers backed by verified sources so that I can trust the information.

### Clinician

> As a clinician, I want cited medical guidelines so that I can validate treatment information quickly.

### Legal Analyst

> As a legal professional, I want references to statutes or legal texts so that I can verify legal interpretations.

### System Administrator

> As an admin, I want to control which documents are included so that only trusted knowledge is used.

---

## 7. System Workflow (High-Level)

1. User submits query
2. Query classification agent identifies domain
3. Retrieval agent fetches relevant passages
4. Validation agent checks evidence quality
5. Generator produces grounded answer
6. Citation auditor verifies references
7. Response returned with citations

---

## 8. Success Criteria

The system is successful when:

* Answers include verified citati
```

## Response snapshot

Implementation of a Domain-Specific Retrieval-Augmented Generation system for medical and legal research. The system includes:

- Models for Query, Response, Citation, User, Document, and Chunk with proper validation
- Specialized agents: Query Classifier, Retrieval Investigator, Evidence Validator, Citation Auditor, and Safety Reviewer
- Services: VectorDB, LLM, Document Processor, and Embedding services
- API endpoints for query processing and document upload
- Comprehensive unit tests covering all components
- Configuration files and Docker support
- A constitutional approach with evidence-first, citation-required, domain-restriction, and safety-over-completeness principles

The implementation follows the project constitution with agent-governed validation, data source authority, and transparency requirements.

## Outcome

- ✅ Impact: Complete implementation of the domain-specific RAG system with all required models, services, agents, and API endpoints
- 🧪 Tests: All 44 unit tests passing, covering models, agents, services, and API endpoints
- 📁 Files: 50+ files created with complete system implementation including models, services, agents, API endpoints, tests, and configuration
- 🔁 Next prompts: Ready for integration testing, document upload functionality, and full system validation
- 🧠 Reflection: The implementation successfully addresses the core problem of hallucinations in LLMs by enforcing strict evidence-based responses with proper citations and safety controls

## Evaluation notes (flywheel)

- Failure modes observed: Pydantic enum handling issues resolved, import structure issues fixed with proper packaging
- Graders run and results (PASS/FAIL): All unit tests pass, system follows constitutional principles
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Integration testing with actual medical/legal documents