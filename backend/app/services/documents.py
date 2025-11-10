"""Document service for file processing and management"""

from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.services.s3 import generate_s3_key, upload_file


async def parse_document_text(file: UploadFile) -> str:
    """
    Parse document and extract text content.

    Args:
        file: Uploaded file

    Returns:
        Extracted text content

    TODO: Implement DOCX parsing using python-docx or similar
    """
    content = await file.read()
    await file.seek(0)  # Reset file pointer for potential re-reading

    # Get file extension
    file_ext = None
    if file.filename:
        file_ext = "." + file.filename.split(".")[-1].lower()

    if file_ext == ".txt":
        # Parse plain text
        try:
            text = content.decode("utf-8")
            return text
        except UnicodeDecodeError:
            return "Error: Unable to decode text file"

    elif file_ext == ".docx":
        # TODO: Parse DOCX using python-docx
        # from docx import Document as DocxDocument
        # doc = DocxDocument(io.BytesIO(content))
        # text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        # return text

        # STUB: Return placeholder
        return "TODO: Parse DOCX content. This is a placeholder for parsed DOCX text."

    else:
        return "Unsupported file format"


async def create_document(
    file: UploadFile, organization_id: int, db: Session
) -> Document:
    """
    Create a document record in the database.

    Args:
        file: Uploaded file
        organization_id: ID of the organization
        db: Database session

    Returns:
        Created Document object
    """
    # Generate S3 key
    s3_key = generate_s3_key("documents", file.filename or "unnamed")

    # Upload to S3 (stubbed)
    await upload_file(file, s3_key)

    # Parse document text
    parsed_text = await parse_document_text(file)

    # Create document record
    document = Document(
        organization_id=organization_id,
        name=file.filename or "Unnamed Document",
        original_filename=file.filename or "unnamed",
        s3_key=s3_key,
        parsed_text=parsed_text,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def list_documents_for_org(org_id: int, db: Session) -> List[Document]:
    """
    List all documents for an organization.

    Args:
        org_id: Organization ID
        db: Database session

    Returns:
        List of Document objects
    """
    documents = (
        db.query(Document)
        .filter(Document.organization_id == org_id)
        .order_by(Document.created_at.desc())
        .all()
    )
    return documents
