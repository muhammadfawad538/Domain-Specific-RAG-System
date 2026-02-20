from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.query_router import router as query_router
from src.api.upload_router import router as upload_router
from src.api.health_router import router as health_router
from src.utils.config import Config
from src.utils.logger import setup_logger

# Validate configuration at startup
Config.validate()

# Set up logger for the API
logger = setup_logger(__name__)

# Create FastAPI app with configuration from spec
app = FastAPI(
    title="Domain-Specific RAG System API",
    description="API for the Domain-Specific Retrieval-Augmented Generation system for medical and legal research",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query_router, prefix="/api", tags=["query"])
app.include_router(upload_router, prefix="/api", tags=["document"])
app.include_router(health_router, prefix="/api", tags=["health"])

# Add event handlers
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Domain-Specific RAG System API")
    # Initialize any required services here

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Domain-Specific RAG System API")
    # Clean up any resources here

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Domain-Specific Retrieval-Augmented Generation System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )