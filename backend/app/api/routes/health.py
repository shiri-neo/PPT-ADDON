"""Health check endpoints"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint to verify service is running"""
    return {"status": "ok"}
