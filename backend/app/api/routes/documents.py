"""Document management endpoints"""

from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_organization
from app.models.user import User
from app.models.organization import Organization
from app.schemas.document import DocumentRead, DocumentCreateResponse
from app.services.documents import create_document, list_documents_for_org

router = APIRouter()


@router.post("/upload", response_model=DocumentCreateResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    Upload a document (txt or docx).
    Stores file metadata and parsed text in database.
    S3 upload is stubbed for now.
    """
    # Validate file type
    allowed_extensions = [".txt", ".docx"]
    file_ext = None
    if file.filename:
        file_ext = "." + file.filename.split(".")[-1].lower()

    if not file_ext or file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}",
        )

    # Create document
    document = await create_document(
        file=file,
        organization_id=current_org.id,
        db=db,
    )

    return DocumentCreateResponse(document=document)


@router.get("", response_model=List[DocumentRead])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    List all documents for the current user's organization.
    """
    documents = list_documents_for_org(org_id=current_org.id, db=db)
    return documents
