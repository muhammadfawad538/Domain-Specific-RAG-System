from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import random
import time
import openai
from anthropic import Anthropic
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("llm_service")

class LLMService(ABC):
    """
    Abstract base class for LLM services.
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


class OpenAILLMService(LLMService):
    """
    OpenAI implementation of LLM service.
    """

    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set for OpenAI service")

        self.model = "gpt-3.5-turbo"  # Default model, can be configured
        self.embedding_model = "text-embedding-ada-002"

    def generate_response(self, prompt: str, context: List[str] = None) -> str:
        """
        Generate a response using OpenAI's API.
        """
        # Build the full prompt with context if provided
        full_prompt = prompt
        if context:
            context_str = "\n".join(context)
            full_prompt = f"Context: {context_str}\n\nQuestion: {prompt}"

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based only on the provided context. If the context does not contain enough information to answer the question, respond with 'Insufficient verified evidence available.'"},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.1,  # Low temperature for more consistent, factual responses
                max_tokens=500
            )
            logger.info("Generated response using OpenAI API")
            return response.choices[0].message['content'].strip()
        except Exception as e:
            logger.error(f"Error generating response with OpenAI: {e}")
            raise

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text using OpenAI.
        """
        try:
            response = openai.Embedding.create(
                input=text,
                model=self.embedding_model
            )
            embedding = response.data[0].embedding
            logger.info(f"Generated embedding of length {len(embedding)} for text")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding with OpenAI: {e}")
            raise


class AnthropicLLMService(LLMService):
    """
    Anthropic implementation of LLM service.
    """

    def __init__(self):
        if not Config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY must be set for Anthropic service")

        self.model = "claude-3-haiku-20240307"  # Default model, can be configured

    def generate_response(self, prompt: str, context: List[str] = None) -> str:
        """
        Generate a response using Anthropic's API.
        """
        # Build the full prompt with context if provided
        full_prompt = prompt
        if context:
            context_str = "\n".join(context)
            full_prompt = f"Context: {context_str}\n\nQuestion: {prompt}"

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.1,
                system="You are a helpful assistant that answers questions based only on the provided context. If the context does not contain enough information to answer the question, respond with 'Insufficient verified evidence available.'",
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )
            logger.info("Generated response using Anthropic API")
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Error generating response with Anthropic: {e}")
            raise

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text.
        Note: Anthropic doesn't provide embedding API, so we'll use OpenAI as fallback if available
        or return an error.
        """
        logger.warning("Anthropic does not provide embedding API, using OpenAI as fallback")
        if Config.OPENAI_API_KEY:
            fallback_service = OpenAILLMService()
            return fallback_service.embed_text(text)
        else:
            raise NotImplementedError("Embedding service not available. Anthropic doesn't provide embedding API.")

    def embed_text(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text.
        Note: Anthropic doesn't provide embedding API, so we'll use a mock approach
        """
        logger.warning("Using mock embedding service for Anthropic (no real embedding API)")

        # Simulate an embedding by creating a deterministic vector based on text
        text_hash = hash(text) % 1000000
        embedding = []
        for i in range(1536):  # Standard embedding size
            # Create pseudo-random but deterministic values based on text and position
            val = ((text_hash * (i + 1)) % 10000) / 10000.0
            embedding.append(val)

        return embedding


class MockLLMService(LLMService):
    """
    Mock implementation of LLM service for testing without API keys.
    """

    def __init__(self):
        logger.info("Initializing Mock LLM Service for testing")
        self.model = "mock-model"

    def generate_response(self, prompt: str, context: List[str] = None) -> str:
        """
        Generate a mock response based on the prompt and optional context.
        """
        logger.info(f"Generating mock response for prompt: {prompt[:30]}...")

        time.sleep(0.05)  # Simulate processing time

        # Simulate different types of responses based on the prompt and context
        # Check if medical terms are in the prompt
        medical_indicators = ["medical", "treatment", "patient", "health", "hospital", "doctor", "clinical", "symptom", "disease", "therapy", "medication", "prescription", "diagnosis"]
        legal_indicators = ["legal", "law", "court", "statute", "statute of limitations", "malpractice", "contract", "agreement", "litigation", "judgment", "ruling", "precedent", "liability", "compliance", "regulatory", "attorney", "lawyer", "doctrine", "jurisdiction", "counsel", "brief"]

        # Check if any medical indicators are in the prompt
        is_medical = any(indicator in prompt.lower() for indicator in medical_indicators)
        # Check if any legal indicators are in the prompt
        is_legal = any(indicator in prompt.lower() for indicator in legal_indicators)

        if is_medical:
            return f"Mock medical response: Based on verified medical literature, the evidence suggests that for '{prompt[:40]}...', further consultation with medical professionals is recommended. [Citation: Mock Medical Journal 2023]"
        elif is_legal:
            return f"Mock legal response: Based on verified legal precedents, for '{prompt[:40]}...', the legal framework indicates certain considerations. [Citation: Mock Legal Statute 2023]"
        elif "insufficient evidence" in prompt.lower() or "unknown" in prompt.lower():
            return "Insufficient verified evidence available."
        else:
            # Default fallback response
            if context and any("legal" in ctx.lower() for ctx in context if ctx):
                return f"Mock legal response: Based on provided context, for '{prompt[:40]}...', legal considerations apply. [Citation: Mock Legal Document 2023]"
            else:
                return f"Mock response generated based on provided context for query: '{prompt[:50]}...'. This response is simulated for testing purposes only. [Citation: Mock Document 2023]"

    def embed_text(self, text: str) -> List[float]:
        """
        Generate a mock embedding for the given text.
        """
        logger.info(f"Generating mock embedding for: {text[:30]}...")

        # Create a deterministic mock embedding based on the text
        # Using Python's hash function to create reproducible "embeddings"
        text_hash = hash(text) % 1000000
        embedding = []

        # Create a 1536-dimensional vector (common embedding size)
        for i in range(1536):
            # Create pseudo-random but deterministic values based on text and position
            val = ((text_hash * (i + 1) * 31) % 10000) / 10000.0
            # Normalize to [-1, 1] range
            val = (val * 2) - 1
            embedding.append(val)

        return embedding


def get_llm_service() -> LLMService:
    """
    Factory function to get the appropriate LLM service based on configuration.
    """
    if Config.OPENAI_API_KEY:
        logger.info("Using OpenAI LLM service")
        return OpenAILLMService()
    elif Config.ANTHROPIC_API_KEY:
        logger.info("Using Anthropic LLM service")
        return AnthropicLLMService()
    elif Config.OLLAMA_MODEL:  # Check if Ollama is configured
        try:
            from .ollama_service import OllamaChatService
            logger.info(f"Using Ollama LLM service with model: {Config.OLLAMA_MODEL}")
            return OllamaChatService(model_name=Config.OLLAMA_MODEL)
        except ImportError:
            logger.warning("Ollama not installed, using Mock service. Install with: pip install ollama")
            return MockLLMService()
    elif Config.GEMINI_API_KEY:  # Check if Gemini is configured
        try:
            from .gemini_service import GeminiChatService
            logger.info("Using Google Gemini LLM service")
            return GeminiChatService()
        except ImportError:
            logger.warning("Google Generative AI not installed, using Mock service. Install with: pip install google-generativeai")
            return MockLLMService()
    else:
        # If no API keys are provided, use the mock service for testing
        logger.warning("No API keys found, using Mock LLM service for testing")
        return MockLLMService()