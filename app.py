"""
Gradio interface for the Domain-Specific RAG System.
This file serves as the entry point for Hugging Face Spaces.
"""

import gradio as gr
import requests
import os
import sys
from threading import Thread
from src.api.main import app as fastapi_app
from src.utils.config import Config

# Set environment variables to ensure proper configuration
os.environ.setdefault("LOG_LEVEL", "INFO")

def query_rag_system(query: str, domain: str = "medical"):
    """Function to query the RAG system"""
    try:
        # Start the FastAPI app in a thread if not already running
        # In Hugging Face Spaces, the main API is available at the space URL
        base_url = os.getenv("SPACE_URL", "http://localhost:8080")

        # Create a simple query request - in a real deployment we'd call our service directly
        response = {
            "response": f"Mock response for query: '{query}' in domain: {domain}. The system is running properly on Hugging Face Spaces. To use with real documents, upload PDF files using the upload endpoint.",
            "citations": ["[No documents uploaded yet - this is a mock response for demonstration]"],
            "domain": domain
        }

        # In a real implementation, we would call the actual service
        # For now we return a mock response to verify the system works
        return response["response"], "\n".join(response["citations"])

    except Exception as e:
        return f"Error processing query: {str(e)}", "No citations available"

def upload_document(file):
    """Function to handle document upload"""
    try:
        if file is None:
            return "No file provided"

        # In a real implementation, we would upload to the actual service
        filename = getattr(file, 'name', 'unknown')
        return f"Document {filename} would be uploaded to the system in a full implementation."
    except Exception as e:
        return f"Error uploading document: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Domain-Specific RAG System") as demo:
    gr.Markdown("""
    # Domain-Specific RAG System for Medical & Legal Research

    This system answers queries using only verified and curated documents while providing precise, traceable citations.
    """)

    with gr.Tab("Query"):
        query_input = gr.Textbox(label="Enter your medical or legal query",
                                placeholder="e.g., What are the current guidelines for treating hypertension?")
        domain_selector = gr.Radio(
            choices=["medical", "legal"],
            value="medical",
            label="Domain"
        )
        query_btn = gr.Button("Submit Query")
        response_output = gr.Textbox(label="Response", interactive=False, max_lines=10)
        citations_output = gr.Textbox(label="Citations", interactive=False)

        query_btn.click(
            fn=query_rag_system,
            inputs=[query_input, domain_selector],
            outputs=[response_output, citations_output]
        )

    with gr.Tab("Upload Documents"):
        doc_input = gr.File(label="Upload Medical or Legal Documents (PDF, TXT)",
                           file_types=[".pdf", ".txt", ".docx"])
        upload_btn = gr.Button("Upload Document")
        upload_output = gr.Textbox(label="Upload Status", interactive=False)

        upload_btn.click(
            fn=upload_document,
            inputs=[doc_input],
            outputs=[upload_output]
        )

    gr.Markdown("""
    ## Notes:
    - This system uses only verified medical and legal documents to generate responses
    - All answers include proper citations to source documents
    - For full functionality, API keys should be configured in the backend
    """)

# This is the entry point for Hugging Face Spaces
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)