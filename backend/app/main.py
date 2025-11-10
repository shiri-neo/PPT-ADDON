"""FastAPI application entry point"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routes import health, auth, documents, presentations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Log startup configuration
logger.info(f"Starting {settings.app_name}")
logger.info(f"Debug mode: {settings.debug}")
logger.info(f"Database: {settings.database_url}")
logger.info(f"CORS origins: {settings.cors_allowed_origins}")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="AI-powered PowerPoint presentation assistant API",
    version="0.1.0",
)

# Configure CORS - Allow all origins in development
# This fixes CORS network errors when frontend calls backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(
    presentations.router, prefix="/presentations", tags=["Presentations"]
)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to PPT AI Assistant API",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
