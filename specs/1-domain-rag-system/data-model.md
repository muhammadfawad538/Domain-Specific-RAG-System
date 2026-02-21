# Data Model for Domain-Specific Retrieval-Augmented Generation System

## Entity: Query
**Description**: A natural language question submitted by a user, including metadata about domain classification

**Fields**:
- `id` (string): Unique identifier for the query
- `content` (string): The natural language question text
- `domain` (enum): Classification as 'medical', 'legal', or 'unknown'
- `user_id` (string): Reference to the user who submitted the query
- `timestamp` (datetime): When the query was submitted
- `status` (enum): Query processing status ('pending', 'processing', 'completed', 'rejected')

**Validation Rules**:
- Content must not be empty
- Domain must be one of the allowed values
- Timestamp must be current or past time

## Entity: Document
**Description**: A vetted source file (PDF or text) containing medical or legal information with associated metadata

**Fields**:
- `id` (string): Unique identifier for the document
- `title` (string): Document title
- `author` (string): Document author
- `publication` (string): Publication source or venue
- `year` (integer): Publication year
- `file_path` (string): Path to stored file
- `file_format` (enum): File format ('PDF', 'TEXT', or others)
- `checksum` (string): File integrity verification
- `domain` (enum): 'medical', 'legal', or 'mixed'
- `created_at` (datetime): When the document was added to the system
- `uploaded_by` (string): User who uploaded the document
- `chunk_count` (integer): Number of semantic chunks derived from the document

**Validation Rules**:
- Title must not be empty
- Year must be a reasonable range (1900 to current year + 1)
- File format must be one of allowed values
- Checksum must be valid

## Entity: Chunk
**Description**: A semantic passage extracted from a document, used for retrieval

**Fields**:
- `id` (string): Unique identifier for the chunk
- `document_id` (string): Reference to the source document
- `content` (string): The text content of the chunk
- `chunk_index` (integer): Sequential position within the document
- `embedding` (array): Vector embedding of the chunk content
- `semantic_boundary` (string): Indicator of semantic completeness
- `created_at` (datetime): When the chunk was created

**Validation Rules**:
- Content must not exceed maximum length
- Document reference must exist
- Embedding vector must have proper dimensions

## Entity: Response
**Description**: The system-generated answer containing information exclusively from retrieved sources with proper citations

**Fields**:
- `id` (string): Unique identifier for the response
- `query_id` (string): Reference to the original query
- `content` (string): The response text
- `status` (enum): Response status ('complete', 'insufficient_evidence', 'rejected')
- `created_at` (datetime): When the response was generated
- `confidence` (float): Confidence score (0.0 to 1.0)
- `disclaimer` (string): Required safety disclaimer for medical/legal information

**Validation Rules**:
- Content must be empty if status is 'insufficient_evidence'
- Confidence must be between 0.0 and 1.0
- Disclaimer is mandatory for medical/legal responses

## Entity: Citation
**Description**: A reference linking a specific claim in the response to the exact source document and location

**Fields**:
- `id` (string): Unique identifier for the citation
- `response_id` (string): Reference to the response containing the citation
- `chunk_id` (string): Reference to the source chunk
- `document_id` (string): Reference to the source document
- `claim_text` (string): The specific text in the response that is being cited
- `citation_text` (string): The corresponding text in the source document
- `confidence` (float): Confidence in the citation's accuracy (0.0 to 1.0)
- `created_at` (datetime): When the citation was created

**Validation Rules**:
- Response and document references must exist
- Confidence must be between 0.0 and 1.0
- Claim text must exist in the associated response
- Citation text must exist in the source chunk

## Entity: User
**Description**: Different types of users (researchers, clinicians, legal professionals, administrators) with appropriate access levels

**Fields**:
- `id` (string): Unique identifier for the user
- `username` (string): User's identifier
- `email` (string): User's email address
- `role` (enum): User role ('researcher', 'clinician', 'legal_professional', 'admin')
- `created_at` (datetime): When the user account was created
- `last_access` (datetime): When the user last accessed the system

**Validation Rules**:
- Email must be valid format
- Role must be one of allowed values
- Username must be unique