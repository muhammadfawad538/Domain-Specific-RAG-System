from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel
import uuid
import os
from datetime import datetime
from src.models.document import Document, DocumentDomain, FileFormat
from src.services.document_processor import DocumentProcessorService
from src.services.embedding_service import EmbeddingService
from src.services.vector_db_service import VectorDBService
from src.utils.parsers import detect_file_format
from src.utils.logger import setup_logger, log_document_processing

router = APIRouter()
logger = setup_logger("upload_router")

# Initialize services
document_processor = DocumentProcessorService()
embedding_service = EmbeddingService()
vector_db_service = VectorDBService()


class UploadRequest(BaseModel):
    title: str
    author: str
    publication: str = None
    year: int = None
    domain: DocumentDomain


class UploadResponse(BaseModel):
    document_id: str
    message: str
    status: str


class DocumentInfo(BaseModel):
    id: str
    title: str
    author: str
    publication: str
    year: int
    domain: DocumentDomain
    chunk_count: int
    created_at: str


class DocumentsListResponse(BaseModel):
    documents: List[DocumentInfo]
    total: int


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    publication: str = Form(None),
    year: int = Form(None),
    domain: DocumentDomain = Form(...)
):
    """
    Upload a medical or legal document to be included in the RAG system's knowledge base.
    """
    try:
        # Generate document ID
        document_id = f"doc_{uuid.uuid4().hex[:8]}"

        # Validate file type
        file_format_str = detect_file_format(file.filename)
        if file_format_str not in ["PDF", "TEXT"]:
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_format_str}. Only PDF and TEXT files are allowed.")

        file_format = FileFormat[file_format_str]

        # Create temporary file path
        temp_file_path = f"./temp_uploads/{document_id}_{file.filename}"
        os.makedirs("./temp_uploads", exist_ok=True)

        # Save uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Log document processing start
        log_document_processing(document_id, "upload_start", "received", {"file_name": file.filename, "file_size": len(content)})

        # Create document object
        document = Document(
            id=document_id,
            title=title,
            author=author,
            publication=publication,
            year=year or datetime.now().year,
            file_path=temp_file_path,
            file_format=file_format,
            checksum=None,  # Could implement checksum later
            domain=domain,
            uploaded_by="temp_user",  # Would be replaced with actual user ID
            chunk_count=0
        )

        # Process the document
        log_document_processing(document_id, "processing", "started")
        processed_chunks = await document_processor.process_document(document)
        log_document_processing(document_id, "processing", "completed", {"chunks_count": len(processed_chunks)})

        # Generate embeddings for the chunks
        log_document_processing(document_id, "embedding", "started")
        embeddings = await embedding_service.generate_embeddings(processed_chunks)
        log_document_processing(document_id, "embedding", "completed", {"embeddings_count": len(embeddings)})

        # Add embeddings to vector database
        log_document_processing(document_id, "indexing", "started")
        vector_db_service.add_embeddings(processed_chunks, embeddings)
        vector_db_service.save_index()  # Persist changes
        log_document_processing(document_id, "indexing", "completed")

        # Update document with chunk count
        document.chunk_count = len(processed_chunks)

        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        # Log completion
        log_document_processing(document_id, "upload_complete", "success", {"final_chunk_count": len(processed_chunks)})

        return UploadResponse(
            document_id=document_id,
            message=f"Document '{title}' uploaded successfully and processed into {len(processed_chunks)} chunks",
            status="success"
        )
    except Exception as e:
        logger.error(f"Error uploading document: {e}")

        # Clean up temporary file if it exists
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        log_document_processing("unknown", "upload_failed", "error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")


@router.get("/documents", response_model=DocumentsListResponse)
async def list_documents():
    """
    Retrieve a list of all documents currently in the system's knowledge base.
    """
    try:
        # In a real implementation, this would fetch from a persistent store
        # For now, we'll return an empty list since we don't have a persistent document store
        # This is a limitation of our current implementation

        # The vector DB service can provide some stats, but not document metadata
        db_stats = vector_db_service.get_stats()

        # In a complete implementation, we would have a document store that maintains
        # metadata about all documents
        documents = []  # This would come from a persistent document store
        total = len(documents)

        return DocumentsListResponse(
            documents=documents,
            total=total
        )
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the document upload system.
    """
    try:
        # Check if services are available
        db_stats = vector_db_service.get_stats()

        health_status = {
            "status": "healthy",
            "components": {
                "document_processor": "initialized",
                "embedding_service": "initialized",
                "vector_db": "healthy" if db_stats else "unavailable"
            },
            "vector_db_stats": db_stats
        }

        return health_status
    except Exception as e:
        logger.error(f"Upload health check failed: {e}")
        return {
            "status": "unavailable",
            "components": {
                "document_processor": "error",
                "embedding_service": "error",
                "vector_db": "error"
            }
        }