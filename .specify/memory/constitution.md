<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.0.0 (initial creation)
- List of modified principles: None (new constitution)
- Added sections: All sections as this is the first version
- Removed sections: None
- Templates requiring updates: None (this is the initial version)
- Follow-up TODOs: None
-->
# Domain-Specific Retrieval-Augmented Generation for Medical & Legal Research Constitution

## Core Principles

### Evidence First (NON-NEGOTIABLE)
Every generated statement must originate from retrieved documents. No unsupported knowledge generation is allowed.
This principle ensures that the system remains grounded in verified evidence and prevents hallucinations by requiring all generated content to be traceable to specific source documents.

### Citation Required (NON-NEGOTIABLE)
All answers must include source attribution. Claims without citations must be rejected.
This principle provides transparency by requiring all responses to include proper attribution to the source documents that support the information provided.

### Domain Restriction (NON-NEGOTIABLE)
Responses must rely ONLY on curated medical or legal sources. External knowledge or model memory must not override retrieved evidence.
This principle maintains the integrity of the system by restricting responses to vetted domain-specific sources, preventing contamination from general web knowledge or model bias.

### Safety Over Completeness (NON-NEGOTIABLE)
If sufficient verified evidence is unavailable, respond: "Insufficient verified evidence available." Never guess.
This principle prioritizes safety and accuracy over providing incomplete or potentially incorrect information when proper evidence is not available.

### Agent-Governed Validation (NON-NEGOTIABLE)
The system follows an agent-controlled RAG pipeline with independent validation stages: Query Classification, Retrieval from vetted corpus, Evidence Validation, Answer Generation, Citation Audit, and Safety Review. Each stage must be independently verifiable.
This principle ensures comprehensive validation through multiple independent verification stages, preventing any single point of failure in the validation process.

### Data Source Authority (NON-NEGOTIABLE)
Only approved sources are allowed: Medical textbooks, peer-reviewed guidelines, clinical standards, legal statutes, court decisions, and official regulatory publications. Prohibited sources include: Blogs, forums, unverified web content, and AI-generated documents.
This principle maintains the credibility of the system by restricting input to authoritative, peer-reviewed sources while explicitly excluding unreliable sources.

## Development Guidelines
Code Quality requirements: Modular agent-based architecture, clear separation between retrieval and generation, deterministic prompts where possible, reproducibility of all experiments, versioning of datasets and embeddings, observability with structured logging of retrieved chunks, citation mappings, validation decisions, and safety flags.

## AI Behavior Constraints
The AI MUST NOT provide diagnosis or legal rulings, invent citations, summarize outside retrieved context, or override validation agents. The AI SHOULD explain uncertainty, prefer precision over verbosity, and highlight conflicting sources.
These constraints ensure the system operates within appropriate boundaries and maintains professional responsibility.

## Subagent Governance
Subagents act as independent auditors with specific responsibilities: Query Classifier (domain routing), Retrieval Investigator (relevance validation), Evidence Validator (source authority check), Citation Auditor (claim verification), and Safety Reviewer (risk prevention). No single agent may bypass another validation stage.
This governance model ensures comprehensive validation through specialized, independent review processes.

## Governance
This constitution supersedes all other development practices and guidelines. All changes affecting retrieval logic, citation rules, safety constraints, or domain scope require review and documentation update. The system success is measured by citation accuracy, retrieval relevance, hallucination rate, expert validation feedback, and safety compliance.

**Version**: 1.0.0 | **Ratified**: 2026-02-19 | **Last Amended**: 2026-02-19
