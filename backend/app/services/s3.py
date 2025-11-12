"""AWS S3 service for file storage (stubbed)"""

import uuid
from typing import Optional

from fastapi import UploadFile

from app.core.config import get_settings

# Note: boto3 import removed - will be added when implementing real S3 functionality
# TODO: Add 'boto3' to requirements.txt when ready to implement actual S3 uploads

settings = get_settings()

# Initialize S3 client (stubbed - won't actually connect)
# TODO: Uncomment when ready to use real S3
# s3_client = boto3.client(
#     "s3",
#     aws_access_key_id=settings.aws_access_key_id,
#     aws_secret_access_key=settings.aws_secret_access_key,
# )


def generate_s3_key(prefix: str, filename: str) -> str:
    """
    Generate a unique S3 object key for a file.

    Args:
        prefix: Folder/prefix for the file (e.g., 'documents', 'images')
        filename: Original filename

    Returns:
        S3 object key string
    """
    unique_id = uuid.uuid4().hex[:8]
    safe_filename = filename.replace(" ", "_")
    return f"{prefix}/{unique_id}_{safe_filename}"


async def upload_file(file: UploadFile, key: str) -> str:
    """
    Upload a file to S3.

    Args:
        file: FastAPI UploadFile object
        key: S3 object key

    Returns:
        S3 object key (or URL in production)

    TODO: Implement actual S3 upload
    """
    # Read file content
    content = await file.read()

    # TODO: Upload to S3
    # s3_client.put_object(
    #     Bucket=settings.aws_s3_bucket_name,
    #     Key=key,
    #     Body=content,
    #     ContentType=file.content_type,
    # )

    # For now, just return the key (stub implementation)
    # In production, this would return the S3 URL or key
    return key


def get_file_url(key: str) -> str:
    """
    Get a pre-signed URL for an S3 object.

    Args:
        key: S3 object key

    Returns:
        Pre-signed URL

    TODO: Implement actual S3 pre-signed URL generation
    """
    # TODO: Generate pre-signed URL
    # url = s3_client.generate_presigned_url(
    #     'get_object',
    #     Params={'Bucket': settings.aws_s3_bucket_name, 'Key': key},
    #     ExpiresIn=3600
    # )
    # return url

    # Stub: return fake URL
    return f"https://{settings.aws_s3_bucket_name}.s3.amazonaws.com/{key}"
