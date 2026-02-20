import asyncio
from typing import List
from src.models.document import Document
from src.models.chunk import Chunk
from src.utils.parsers import extract_text_from_pdf, extract_text_from_txt, create_chunks_from_document
from src.utils.logger import setup_logger

logger = setup_logger("document_processor")

class DocumentProcessorService:
    """
    Service for processing documents into chunks for the RAG system.
    """

    def __init__(self):
        self.supported_formats = {".pdf", ".txt"}

    async def process_document(self, document: Document) -> List[Chunk]:
        """
        Process a document into chunks.

        Args:
            document: The document to process

        Returns:
            List of Chunk objects created from the document
        """
        try:
            logger.info(f"Starting processing of document: {document.id} - {document.title}")

            # Extract text based on file format
            if document.file_format.lower() == "pdf":
                content = extract_text_from_pdf(document.file_path)
            elif document.file_format.lower() == "text":
                content = extract_text_from_txt(document.file_path)
            else:
                raise ValueError(f"Unsupported file format: {document.file_format}")

            # Create chunks from the content
            chunks = create_chunks_from_document(
                doc_id=document.id,
                content=content,
                max_chunk_size=1000,  # Using default values, could be configurable
                overlap=200
            )

            logger.info(f"Successfully processed document {document.id} into {len(chunks)} chunks")
            return chunks

        except Exception as e:
            logger.error(f"Error processing document {document.id}: {e}")
            raise

    async def process_documents_batch(self, documents: List[Document]) -> List[List[Chunk]]:
        """
        Process multiple documents in parallel.

        Args:
            documents: List of documents to process

        Returns:
            List of lists of chunks (one list per document)
        """
        logger.info(f"Starting batch processing of {len(documents)} documents")

        # Process documents concurrently
        tasks = [self.process_document(doc) for doc in documents]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions that occurred during processing
        processed_chunks = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing document {documents[i].id}: {result}")
                # Decide whether to raise the exception or continue with other documents
                # For now, we'll continue processing other documents
                processed_chunks.append([])
            else:
                processed_chunks.append(result)

        logger.info(f"Completed batch processing of {len(documents)} documents")
        return processed_chunks

    def validate_document(self, document: Document) -> bool:
        """
        Validate that a document meets the requirements for processing.

        Args:
            document: The document to validate

        Returns:
            True if document is valid, False otherwise
        """
        try:
            # Check if file exists
            import os
            if not os.path.exists(document.file_path):
                logger.error(f"Document file does not exist: {document.file_path}")
                return False

            # Check if file format is supported
            if document.file_format.lower() not in self.supported_formats:
                logger.error(f"Unsupported file format: {document.file_format}")
                return False

            # Check if document domain is valid
            valid_domains = {"medical", "legal", "mixed"}
            if document.domain.lower() not in valid_domains:
                logger.error(f"Invalid document domain: {document.domain}")
                return False

            # Additional validation checks can be added here

            logger.info(f"Document {document.id} passed validation")
            return True

        except Exception as e:
            logger.error(f"Error validating document {document.id}: {e}")
            return False