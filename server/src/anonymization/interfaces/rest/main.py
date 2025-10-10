"""FastAPI application - Main entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import anonymization, health

# Create FastAPI application
app = FastAPI(
    title="GDPR Anonymizer API",
    description="Production-ready text anonymization system with hexagonal architecture",
    version="0.4.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(anonymization.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "GDPR Anonymizer API",
        "version": "0.4.0",
        "docs": "/docs",
        "health": "/health"
    }
