from setuptools import setup, find_packages

setup(
    name="domain-specific-rag-system",
    version="1.0.0",
    description="Domain-Specific Retrieval-Augmented Generation System for Medical and Legal Research",
    author="AI Assistant",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "faiss-cpu>=1.7.0",
        "pydantic>=2.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "spacy>=3.7.0",
        "PyMuPDF>=1.20.0",
        "python-multipart>=0.0.9",
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "openai>=1.0.0",
        "anthropic>=0.20.0",
        "numpy>=1.20.0",
        "pandas>=2.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.15.0",
        ],
    },
    python_requires=">=3.8",
)