"""
How to Use Free LLM APIs with the Domain-Specific RAG System

This guide shows how to configure the system to use free LLM services instead of the mock service.
"""

## 1. OLLAMA (RECOMMENDED - FREE LOCAL MODELS)
"""
Ollama provides free access to powerful open-source models like Llama, Mistral, etc.
Models run locally on your machine.

Installation:
1. Go to https://ollama.ai and download the appropriate installer
2. Install Ollama on your system
3. Pull a model you want to use:

   # For general purpose
   ollama pull llama3.2

   # Or for other models
   ollama pull mistral
   ollama pull phi3
   ollama pull gemma2

4. Create/update your .env file with:
   OLLAMA_MODEL=llama3.2

5. Install the Python client:
   pip install ollama

6. Run the server as usual:
   python -m src.api.main
"""

## 2. HUGGINGFACE INFERENCE API (LIMITED FREE TIER)
"""
Hugging Face provides free inference for many models with rate limits.

1. Get an access token from https://huggingface.co/settings/tokens
2. Add to your .env file:
   HUGGINGFACE_API_TOKEN=your_token_here

3. Install the client:
   pip install huggingface_hub

4. Then you can use models like:
   - google/flan-t5-xxl
   - facebook/blenderbot-400M-distill
   - gpt2
"""

## 3. GOOGLE GEMINI (FREE TIER WITH QUOTA)
"""
Google Gemini offers a free tier with API access.

1. Get an API key from https://aistudio.google.com/
2. Add to your .env file:
   GEMINI_API_KEY=your_key_here

3. Install the client:
   pip install google-generativeai

4. Create a Gemini service implementation (would require additional code)
"""

## 4. CREATING A GEMINI INTEGRATION
"""
If you want to use Google Gemini, here's a basic service structure:

import google.generativeai as genai
from src.utils.config import Config

class GeminiLLMService(LLMService):
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_response(self, prompt: str, context: List[str] = None) -> str:
        full_prompt = prompt
        if context:
            context_str = "\n".join(context)
            full_prompt = f"Context: {context_str}\n\nQuestion: {prompt}"

        response = self.model.generate_content(full_prompt)
        return response.text

    def embed_text(self, text: str) -> List[float]:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
"""

## 5. CONFIGURATION EXAMPLE
"""
Create a .env file in your project root:

# For Ollama (recommended - free and runs locally)
OLLAMA_MODEL=llama3.2

# OR for OpenAI (requires paid account)
# OPENAI_API_KEY=your_openai_api_key

# OR for Anthropic (requires paid account)
# ANTHROPIC_API_KEY=your_anthropic_api_key

# OR for HuggingFace (requires token)
# HUGGINGFACE_API_TOKEN=your_hf_token

# System configurations
VECTOR_DB_PATH=./data/vector_db
DOCUMENT_STORAGE_PATH=./data/documents
LOG_LEVEL=INFO
"""

## 6. TESTING WITH OLLAMA
"""
Once you've set up Ollama:

1. Make sure Ollama is running on your system
2. Pull a model: ollama pull llama3.2
3. Set OLLAMA_MODEL in your .env file
4. Start the server: python -m src.api.main
5. Test the query endpoint:

curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the current medical guidelines for treating hypertension?",
    "user_id": "test_user_123",
    "domain": "medical"
  }'
"""

print(__doc__)