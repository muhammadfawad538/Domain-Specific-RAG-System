import pytest
from unittest.mock import Mock, patch
from src.services.llm_service import OpenAILLMService, AnthropicLLMService, get_llm_service
from src.utils.config import Config


def test_openai_llm_service_initialization():
    """Test initialization of OpenAILLMService when API key is available."""
    # Temporarily set the OpenAI API key for testing
    original_key = Config.OPENAI_API_KEY
    Config.OPENAI_API_KEY = "test-key"

    try:
        service = OpenAILLMService()
        assert service is not None
    finally:
        # Restore original key
        Config.OPENAI_API_KEY = original_key


def test_anthropic_llm_service_initialization():
    """Test initialization of AnthropicLLMService when API key is available."""
    # Temporarily set the Anthropic API key for testing
    original_key = Config.ANTHROPIC_API_KEY
    Config.ANTHROPIC_API_KEY = "test-key"

    try:
        service = AnthropicLLMService()
        assert service is not None
    finally:
        # Restore original key
        Config.ANTHROPIC_API_KEY = original_key


def test_openai_llm_service_without_api_key():
    """Test that OpenAILLMService raises error when API key is not set."""
    # Temporarily unset the OpenAI API key for testing
    original_key = Config.OPENAI_API_KEY
    Config.OPENAI_API_KEY = None

    try:
        with pytest.raises(ValueError):
            OpenAILLMService()
    finally:
        # Restore original key
        Config.OPENAI_API_KEY = original_key


def test_anthropic_llm_service_without_api_key():
    """Test that AnthropicLLMService raises error when API key is not set."""
    # Temporarily unset the Anthropic API key for testing
    original_key = Config.ANTHROPIC_API_KEY
    Config.ANTHROPIC_API_KEY = None

    try:
        with pytest.raises(ValueError):
            AnthropicLLMService()
    finally:
        # Restore original key
        Config.ANTHROPIC_API_KEY = original_key


def test_get_llm_service_openai():
    """Test the factory function returns OpenAI service when available."""
    # Temporarily set OpenAI API key
    original_openai_key = Config.OPENAI_API_KEY
    original_anthropic_key = Config.ANTHROPIC_API_KEY

    Config.OPENAI_API_KEY = "test-key"
    Config.ANTHROPIC_API_KEY = None

    try:
        service = get_llm_service()
        assert isinstance(service, OpenAILLMService)
    finally:
        # Restore original keys
        Config.OPENAI_API_KEY = original_openai_key
        Config.ANTHROPIC_API_KEY = original_anthropic_key


def test_get_llm_service_anthropic():
    """Test the factory function returns Anthropic service when OpenAI is not available."""
    # Temporarily set Anthropic API key and unset OpenAI key
    original_openai_key = Config.OPENAI_API_KEY
    original_anthropic_key = Config.ANTHROPIC_API_KEY

    Config.OPENAI_API_KEY = None
    Config.ANTHROPIC_API_KEY = "test-key"

    try:
        service = get_llm_service()
        assert isinstance(service, AnthropicLLMService)
    finally:
        # Restore original keys
        Config.OPENAI_API_KEY = original_openai_key
        Config.ANTHROPIC_API_KEY = original_anthropic_key


def test_get_llm_service_error():
    """Test that factory function returns Mock service when no API keys are available."""
    # Temporarily unset all API keys
    original_openai_key = Config.OPENAI_API_KEY
    original_anthropic_key = Config.ANTHROPIC_API_KEY
    original_ollama_model = Config.OLLAMA_MODEL
    original_gemini_key = Config.GEMINI_API_KEY

    Config.OPENAI_API_KEY = None
    Config.ANTHROPIC_API_KEY = None
    Config.OLLAMA_MODEL = None
    Config.GEMINI_API_KEY = None

    try:
        from src.services.llm_service import MockLLMService
        service = get_llm_service()
        assert isinstance(service, MockLLMService)
    finally:
        # Restore original keys
        Config.OPENAI_API_KEY = original_openai_key
        Config.ANTHROPIC_API_KEY = original_anthropic_key
        Config.OLLAMA_MODEL = original_ollama_model
        Config.GEMINI_API_KEY = original_gemini_key


# Mock the actual API calls to avoid making real requests
@patch('openai.ChatCompletion.create')
def test_openai_generate_response(mock_openai_call):
    """Test OpenAI LLM service response generation."""
    # Mock the API response
    mock_openai_call.return_value = Mock()
    mock_openai_call.return_value.choices = [Mock()]
    mock_openai_call.return_value.choices[0].message = {'content': 'Test response'}

    # Temporarily set OpenAI API key
    original_key = Config.OPENAI_API_KEY
    Config.OPENAI_API_KEY = "test-key"

    try:
        service = OpenAILLMService()
        response = service.generate_response("Test prompt")

        assert response == "Test response"
    finally:
        # Restore original key
        Config.OPENAI_API_KEY = original_key


@patch('openai.Embedding.create')
def test_openai_embed_text(mock_openai_embedding):
    """Test OpenAI LLM service embedding generation."""
    # Mock the API response
    mock_response = Mock()
    mock_response.data = [Mock()]
    mock_response.data[0].embedding = [0.1, 0.2, 0.3]
    mock_openai_embedding.return_value = mock_response

    # Temporarily set OpenAI API key
    original_key = Config.OPENAI_API_KEY
    Config.OPENAI_API_KEY = "test-key"

    try:
        service = OpenAILLMService()
        embedding = service.embed_text("Test text")

        assert embedding == [0.1, 0.2, 0.3]
    finally:
        # Restore original key
        Config.OPENAI_API_KEY = original_key