from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os

# Check if google-generativeai is available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("gemini_service")

class GeminiLLMService(ABC):
    """
    Abstract base class for Google Gemini LLM services.
    """

    @abstractmethod
    def generate_response(self, prompt: str, context: List[str] = None) -> str:
        """
        Generate a response based on the prompt and optional context.
        """
        pass

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text.
        """
        pass


class GeminiChatService(GeminiLLMService):
    """
    Google Gemini implementation of LLM service.
    """

    def __init__(self):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai is not installed. Install with: pip install google-generativeai")

        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY must be set for Gemini service")

        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.embedding_model = "models/embedding-001"
        logger.info("Initialized Gemini service")

    def generate_response(self, prompt: str, context: List[str] = None) -> str:
        """
        Generate a response using Google Gemini.
        """
        # Build the full prompt with context if provided
        full_prompt = prompt
        if context:
            context_str = "\n".join(context)
            full_prompt = f"Context: {context_str}\n\nQuestion: {prompt}"

        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.1,  # Low temperature for more factual responses
                    "max_output_tokens": 800
                }
            )

            if response.text:
                logger.info("Generated response using Google Gemini")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty response")
                return "Insufficient verified evidence available."

        except Exception as e:
            logger.error(f"Error generating response with Gemini: {e}")
            return "Error: Could not generate response using Gemini."

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding using Google's embedding service.
        """
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            embedding = result['embedding']
            logger.info(f"Generated embedding of length {len(embedding)} for text")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding with Gemini: {e}")
            # Return a mock embedding as fallback
            return [0.0] * 1536