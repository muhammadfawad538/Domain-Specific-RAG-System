# Use official Python runtime as base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gradio for Hugging Face Spaces interface
RUN pip install gradio

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p data/vector_db data/documents data/metadata temp_uploads

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]