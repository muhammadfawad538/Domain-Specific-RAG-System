# Free LLM Integration Guide for Domain-Specific RAG System

This guide shows how to set up and use free or low-cost LLM services with your Domain-Specific RAG System instead of the mock service.

## Option 1: Ollama (Recommended - Completely Free)

### Installation
1. **Download and Install Ollama:**
   - Visit [https://ollama.ai](https://ollama.ai)
   - Download the installer for your operating system (Windows, macOS, or Linux)
   - Run the installer and follow the instructions

2. **Start Ollama:**
   - On Windows: Run the Ollama application
   - On Mac/Linux: Ollama should start automatically after installation

3. **Pull a Model:**
   Open a terminal/command prompt and run:
   ```bash
   # For a good general-purpose model
   ollama pull llama3.2

   # Alternative models you can try
   ollama pull mistral
   ollama pull phi3
   ollama pull gemma2
   ```

4. **Install Python Client:**
   ```bash
   pip install ollama
   ```

5. **Configure the System:**
   Create or update your `.env` file in the project root:
   ```env
   OLLAMA_MODEL=llama3.2
   ```

6. **Run the System:**
   ```bash
   python -m src.api.main
   ```

## Option 2: Google Gemini (Free Tier Available)

### Setup
1. **Get API Key:**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account
   - Create an API key

2. **Install Python Client:**
   ```bash
   pip install google-generativeai
   ```

3. **Configure the System:**
   Add to your `.env` file:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Option 3: Hugging Face (Free Tier with Rate Limits)

### Setup
1. **Get Access Token:**
   - Go to [Hugging Face](https://huggingface.co/settings/tokens)
   - Create an access token

2. **Install Python Client:**
   ```bash
   pip install huggingface_hub
   ```

3. **Configure the System:**
   Add to your `.env` file:
   ```env
   HUGGINGFACE_API_TOKEN=your_token_here
   ```

## Configuration Priority Order

The system will use LLMs in this order:

1. **OpenAI** (if `OPENAI_API_KEY` is set)
2. **Anthropic** (if `ANTHROPIC_API_KEY` is set)
3. **Ollama** (if `OLLAMA_MODEL` is set) ← Recommended free option
4. **Google Gemini** (if `GEMINI_API_KEY` is set)
5. **Mock Service** (fallback when no keys are set)

## Example .env File

For Ollama (completely free):
```env
OLLAMA_MODEL=llama3.2

# System configurations
VECTOR_DB_PATH=./data/vector_db
DOCUMENT_STORAGE_PATH=./data/documents
LOG_LEVEL=INFO
```

For Google Gemini (free tier with usage limits):
```env
GEMINI_API_KEY=your_google_api_key_here

# System configurations
VECTOR_DB_PATH=./data/vector_db
DOCUMENT_STORAGE_PATH=./data/documents
LOG_LEVEL=INFO
```

## Testing Your Setup

Once configured, test the system:

```bash
# Start the server
python -m src.api.main

# Test a query in a new terminal
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the current medical guidelines for treating hypertension?",
    "user_id": "test_user_123",
    "domain": "medical"
  }'
```

## Recommended Models for Your Use Case

### For Ollama:
- `llama3.2` - Good general purpose model
- `mistral` - Strong in reasoning and analysis
- `phi3` - Lightweight but effective
- `gemma2` - Google's open model

### For Gemini:
- Excellent for research and analysis tasks
- Good at citing sources and providing structured responses
- Has good safety features built-in

## Troubleshooting

1. **Ollama not working:**
   - Verify Ollama is running
   - Check if the model was pulled: `ollama list`
   - Try running: `ollama run llama3.2`

2. **API keys not recognized:**
   - Make sure your `.env` file is in the project root
   - Restart the server after changing `.env`
   - Verify the variable names match exactly

3. **Rate limiting:**
   - For free tiers, implement rate limiting in production
   - Consider caching responses for common queries

The Ollama option is recommended as it's completely free, runs locally, and provides good quality responses for research applications.