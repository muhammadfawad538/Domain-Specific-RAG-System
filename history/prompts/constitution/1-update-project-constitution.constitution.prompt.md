---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-02-19
surface: agent
model: if/qwen3-coder-plus
feature: none
branch: master
user: FRIENDS PC
command: sp.constitution
labels: [constitution,specification,governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
for my this project E:\Ass-2-it\myproject  is  Project Constitution

Domain-Specific Retrieval-Augmented Generation for Medical & Legal Research

1. Project Purpose

This project builds a domain-restricted Retrieval-Augmented Generation (RAG) system designed for medical and legal research.

The system MUST:

Reduce hallucinations

Ground answers strictly in verified documents

Provide transparent citations

Support evidence-based decision making

The system is research assistance, NOT professional advice.

2. Core Principles (NON-NEGOTIABLE)
✅ Evidence First

Every generated statement must originate from retrieved documents.

No unsupported knowledge generation is allowed.

✅ Citation Required

All answers must include source attribution.

Claims without citations must be rejected.

✅ Domain Restriction

Responses must rely ONLY on curated medical or legal sources.

External knowledge or model memory must not override retrieved evidence.

✅ Safety Over Completeness

If sufficient verified evidence is unavailable:

Respond: "Insufficient verified evidence available."

Never guess.

3. System Architecture Rules

The system follows an agent-controlled RAG pipeline:

Query Classification

Retrieval from vetted corpus

Evidence Validation

Answer Generation

Citation Audit

Safety Review

Each stage must be independently verifiable.

4. Data Governance

Allowed sources:

Medical textbooks

Peer-reviewed guidelines

Clinical standards

Legal statutes

Court decisions

Official regulatory publications

Not allowed:

Blogs

Forums

Unverified web content

AI-generated documents

5. Development Guidelines
Code Quality

Modular agent-based architecture

Clear separation between retrieval and generation

Deterministic prompts where possible

Reproducibility

All experiments must be reproducible.

Version datasets and embeddings.

Observability

System must log:

Retrieved chunks

Citation mappings

Validation decisions

Safety flags

6. AI Behavior Constraints

The AI MUST NOT:

Provide diagnosis or legal rulings

Invent citations

Summarize outside retrieved context

Override validation agents

The AI SHOULD:

Explain uncertainty

Prefer precision over verbosity

Highlight conflicting sources

7. Subagent Governance

Subagents act as independent auditors:

Agent    Responsibility
Query Classifier    Domain routing
Retrieval Investigator    Relevance validation
Evidence Validator    Source authority check
Citation Auditor    Claim verification
Safety Reviewer    Risk prevention

No single agent may bypass another validation stage.

8. Evaluation Standards

System success measured by:

Citation accuracy

Retrieval relevance

Hallucination rate

Expert validation feedback

Safety compliance

9. Change Management

Any change affecting:

retrieval logic

citation rules

safety constraints

domain scope

requires review and documentation update.

10. Guiding Philosophy

Accuracy is more important than fluency.
Transparency is more important than confidence.
Verified knowledge is more important than fast answers.
```

## Response snapshot

The project constitution at `.specify/memory/constitution.md` has been successfully updated with the new content for a Domain-Specific Retrieval-Augmented Generation for Medical & Legal Research project. The template placeholders were filled with the provided principles and guidelines, creating a comprehensive constitution that emphasizes evidence-first generation, citation requirements, domain restriction, safety over completeness, agent-governed validation, and data source authority. The file now includes core principles, development guidelines, AI behavior constraints, and subagent governance requirements with version tracking set to 1.0.0.

## Outcome

- ✅ Impact: Created initial project constitution with comprehensive governance principles for medical & legal RAG system
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new constitution content
- 🔁 Next prompts: None needed - constitution is complete
- 🧠 Reflection: The constitution establishes clear non-negotiable principles for evidence-based, safety-focused information retrieval in sensitive domains

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A