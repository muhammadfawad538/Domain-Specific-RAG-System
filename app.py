"""
Minimal Gradio interface for the Domain-Specific RAG System.
This file serves as the entry point for Hugging Face Spaces.
Designed for fast startup to avoid timeout issues.
"""

import gradio as gr
import os

def query_rag_system(query: str, domain: str = "medical"):
    """Simple function to demonstrate the RAG system"""
    if not query.strip():
        return "Please enter a query.", "No query provided"

    # Simple mock response without heavy processing
    response = f"System is running! Query: '{query}' in {domain} domain. For full functionality, configure API keys and upload documents."
    citations = "[This is a demonstration response - system ready for document uploads]"

    return response, citations

def upload_document(file):
    """Simple document upload handler"""
    if file is None:
        return "No file selected"

    filename = getattr(file, 'name', 'unknown')
    return f"File '{filename}' would be processed in a full implementation."

# Create a minimal Gradio interface
with gr.Blocks(title="Domain-Specific RAG System") as demo:
    gr.Markdown("# Domain-Specific RAG System (Minimal Version)")
    gr.Markdown("Medical & Legal Research with Verified Citations")

    with gr.Tab("Query"):
        query_input = gr.Textbox(
            label="Enter your query",
            placeholder="Type a medical or legal question..."
        )
        domain_selector = gr.Dropdown(
            choices=["medical", "legal"],
            value="medical",
            label="Domain"
        )
        query_btn = gr.Button("Get Response", variant="primary")
        response_output = gr.Textbox(label="Response", max_lines=5)
        citations_output = gr.Textbox(label="Citations", max_lines=3)

        query_btn.click(
            query_rag_system,
            inputs=[query_input, domain_selector],
            outputs=[response_output, citations_output]
        )

    with gr.Tab("Upload"):
        doc_input = gr.File(
            label="Upload Documents",
            file_types=[".pdf", ".txt", ".docx"]
        )
        upload_btn = gr.Button("Process Document")
        upload_output = gr.Textbox(label="Status")

        upload_btn.click(
            upload_document,
            inputs=[doc_input],
            outputs=[upload_output]
        )

    gr.Markdown("System ready! This is the minimal version for Hugging Face Spaces.")

# Launch with proper port for Hugging Face Spaces
if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        show_error=True
    )