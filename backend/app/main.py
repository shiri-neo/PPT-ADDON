"""FastAPI application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routes import health, auth, documents, presentations

settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="AI-powered PowerPoint presentation assistant API",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
