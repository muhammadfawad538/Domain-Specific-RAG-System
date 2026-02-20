from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import ollama
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("ollama_service")

class OllamaLLMService(ABC):
    """
    Abstract base class for Ollama LLM services.
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


class OllamaChatService(OllamaLLMService):
    """
    Ollama implementation of LLM service using local models.
    """

    def __init__(self, model_name: str = "llama3.2"):
        self.model = model_name
        logger.info(f"Initializing Ollama service with model: {self.model}")

    def generate_response(self, prompt: str, context: List[str] = None) -> str:
        """
        Generate a response using local Ollama model.
        """
        # Build the full prompt with context if provided
        full_prompt = prompt
        if context:
            context_str = "\n".join(context)
            full_prompt = f"Context: {context_str}\n\nQuestion: {prompt}"

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a helpful assistant that answers questions based only on the provided context. If the context does not contain enough information to answer the question, respond with "Insufficient verified evidence available."'
                    },
                    {
                        'role': 'user',
                        'content': full_prompt
                    }
                ]
            )
            logger.info("Generated response using Ollama")
            return response['message']['content'].strip()
        except Exception as e:
            logger.error(f"Error generating response with Ollama: {e}")
            return "Error: Could not generate response using local model."

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding using Ollama's embedding capability.
        """
        try:
            response = ollama.embeddings(model=self.model, prompt=text)
            embedding = response.get('embedding', [])
            logger.info(f"Generated embedding of length {len(embedding)} for text")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding with Ollama: {e}")
            # Return a mock embedding as fallback
            return [0.0] * 1536