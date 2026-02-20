import fitz  # PyMuPDF
import spacy
from typing import List, Tuple
import re
from pathlib import Path
from src.utils.logger import setup_logger
from src.models.chunk import Chunk
import uuid

logger = setup_logger("document_parsers")

# Load spaCy model for semantic processing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy 'en_core_web_sm' model not found. Please install with: python -m spacy download en_core_web_sm")
    nlp = None

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file using PyMuPDF.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        logger.info(f"Extracted {len(text)} characters from PDF: {file_path}")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}")
        raise


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text content from a text file.

    Args:
        file_path: Path to the text file

    Returns:
        Extracted text content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        logger.info(f"Extracted {len(content)} characters from TXT: {file_path}")
        return content
    except Exception as e:
        logger.error(f"Error extracting text from TXT {file_path}: {e}")
        raise


def chunk_text_semantically(text: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into semantically coherent chunks using spaCy for sentence segmentation.

    Args:
        text: The text to chunk
        max_chunk_size: Maximum number of characters per chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if not nlp:
        logger.warning("spaCy model not loaded, falling back to simple sentence-based chunking")
        return _simple_chunk_text(text, max_chunk_size, overlap)

    try:
        doc = nlp(text)
        sentences = [sent.text for sent in doc.sents]

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # Check if adding the sentence would exceed the chunk size
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence + " "
            else:
                # If the current chunk is not empty, save it
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # If the sentence itself is longer than max_chunk_size, split it
                if len(sentence) > max_chunk_size:
                    # Split the long sentence into smaller parts
                    sentence_chunks = _split_long_sentence(sentence, max_chunk_size, overlap)
                    chunks.extend(sentence_chunks[:-1])  # Add all but the last part to chunks
                    current_chunk = sentence_chunks[-1]  # Start new chunk with the last part
                else:
                    # Start a new chunk with the current sentence
                    current_chunk = sentence + " "

        # Add the last chunk if it's not empty
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        logger.info(f"Created {len(chunks)} semantic chunks from text")
        return chunks

    except Exception as e:
        logger.error(f"Error during semantic chunking: {e}")
        # Fall back to simple chunking if spaCy fails
        return _simple_chunk_text(text, max_chunk_size, overlap)


def _split_long_sentence(sentence: str, max_chunk_size: int, overlap: int) -> List[str]:
    """
    Split a sentence that is longer than max_chunk_size into smaller parts.
    """
    if len(sentence) <= max_chunk_size:
        return [sentence]

    chunks = []
    start = 0
    while start < len(sentence):
        end = start + max_chunk_size
        if end >= len(sentence):
            chunks.append(sentence[start:])
            break

        # Try to find a space to break at to avoid cutting words
        while end > start and sentence[end] != ' ' and end > start + max_chunk_size - overlap:
            end -= 1

        if end == start + max_chunk_size - overlap:
            # If we couldn't find a space, just cut at max_chunk_size
            end = start + max_chunk_size

        chunks.append(sentence[start:end].strip())
        start = end - overlap if end > start else start + max_chunk_size

    return chunks


def _simple_chunk_text(text: str, max_chunk_size: int, overlap: int) -> List[str]:
    """
    Simple fallback method to chunk text by character count.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chunk_size

        # If we've reached the end of the text
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Try to find a sentence or paragraph boundary near the end
        chunk_end = end
        for i in range(end, max(start, end - 100), -1):  # Look back up to 100 chars
            if text[i] in '.!?':
                chunk_end = i + 1
                break
            elif text[i] == '\n':
                chunk_end = i
                break

        if chunk_end == end:
            # If no good break point found, just cut at max_chunk_size
            chunk_end = end

        chunk_text = text[start:chunk_end].strip()
        chunks.append(chunk_text)

        # Move start position with overlap
        start = max(chunk_end - overlap, start + 1)  # Ensure progress

    # Filter out empty chunks
    chunks = [chunk for chunk in chunks if chunk.strip()]
    logger.info(f"Created {len(chunks)} chunks using simple method")
    return chunks


def create_chunks_from_document(doc_id: str, content: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[Chunk]:
    """
    Create Chunk objects from document content.

    Args:
        doc_id: Document ID to associate with chunks
        content: Document content to chunk
        max_chunk_size: Maximum size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of Chunk objects
    """
    text_chunks = chunk_text_semantically(content, max_chunk_size, overlap)

    chunks = []
    for i, text in enumerate(text_chunks):
        chunk = Chunk(
            id=f"chunk_{doc_id}_{i}",
            document_id=doc_id,
            content=text,
            chunk_index=i,
            embedding=None,  # Embeddings will be added later
            semantic_boundary=None  # Could be used to indicate if chunk ends at semantic boundary
        )
        chunks.append(chunk)

    logger.info(f"Created {len(chunks)} Chunk objects for document {doc_id}")
    return chunks


def detect_file_format(file_path: str) -> str:
    """
    Detect the format of a file based on its extension.

    Args:
        file_path: Path to the file

    Returns:
        Detected file format as a string
    """
    extension = Path(file_path).suffix.lower()

    format_mapping = {
        '.pdf': 'PDF',
        '.txt': 'TEXT',
        '.doc': 'DOC',
        '.docx': 'DOCX'
    }

    return format_mapping.get(extension, 'UNKNOWN')