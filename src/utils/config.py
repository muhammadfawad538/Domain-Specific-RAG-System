import os
from dotenv import load_dotenv
from src.utils.logger import setup_logger

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to store environment variables and settings."""

    # LLM Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")  # e.g., "llama3.2", "mistral", etc.
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Google Gemini API key

    # Database Configuration
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_db")

    # Document Storage Configuration
    DOCUMENT_STORAGE_PATH = os.getenv("DOCUMENT_STORAGE_PATH", "./data/documents")

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Performance Configuration
    MAX_QUERY_RESPONSE_TIME = float(os.getenv("MAX_QUERY_RESPONSE_TIME", "3.0"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Validation Configuration
    MIN_CONFIDENCE_SCORE = float(os.getenv("MIN_CONFIDENCE_SCORE", "0.7"))

    @classmethod
    def validate(cls):
        """Validate that required configurations are present."""
        # In testing mode, we allow no API keys to use the mock service
        # Only raise error if both keys are missing and we're in production mode
        # For this implementation, we'll allow the mock service to be used by default
        # Import here to avoid circular import
        from src.utils.logger import setup_logger
        logger = setup_logger("config")
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY and not cls.OLLAMA_MODEL and not cls.GEMINI_API_KEY:
            logger.warning("No API keys found. The system will use the Mock LLM service for testing.")

        # Validate paths exist or can be created
        for path in [cls.VECTOR_DB_PATH, cls.DOCUMENT_STORAGE_PATH]:
            os.makedirs(path, exist_ok=True)