"""FastAPI application - Main entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .routers import anonymization, health

# Create FastAPI application
app = FastAPI(
    title="GDPR Anonymizer API",
    description="Production-ready text anonymization system with hexagonal architecture",
    version="0.5.0",
    docs_url="/api/docs",      # Move docs to /api/docs
    redoc_url="/api/redoc"     # Move redoc to /api/redoc
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router)
app.include_router(anonymization.router)

# Serve static files (UI)
static_dir = Path("/app/static")
if static_dir.exists():
    # Mount assets directory for static resources
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

    @app.get("/")
    async def serve_spa():
        """Serve the SPA index.html for the root path."""
        return FileResponse(static_dir / "index.html")

    @app.get("/{full_path:path}")
    async def serve_spa_routes(full_path: str):
        """Catch-all route to serve SPA for client-side routing."""
        # Exclude API routes
        if full_path.startswith("api/"):
            return {"error": "Not found"}

        # Check if file exists
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # Fallback to index.html for SPA routing
        return FileResponse(static_dir / "index.html")
else:
    # Fallback API info endpoint when static files don't exist (dev mode)
    @app.get("/")
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "GDPR Anonymizer API",
            "version": "0.5.0",
            "docs": "/api/docs",
            "health": "/health"
        }
