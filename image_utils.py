import uuid
from io import BytesIO
import logging

from PIL import Image, ImageOps

import boto3
from starlette.concurrency import run_in_threadpool

from config import settings

logger = logging.getLogger(__name__)


def _get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY_ID.get_secret_value()
        if settings.S3_ACCESS_KEY_ID
        else None,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY.get_secret_value()
        if settings.S3_SECRET_ACCESS_KEY
        else None,
        region_name=settings.S3_REGION_NAME,
        endpoint_url=settings.S3_ENDPOINT_URL,
    )


def process_profile_picture(content: bytes) -> tuple[bytes, str]:
    with Image.open(BytesIO(content)) as original:
        # Correct orientation based on EXIF data and resize to 300x300 while maintaining aspect ratio
        img = ImageOps.exif_transpose(original)
        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        # Convert to RGB if the image has an alpha channel or is in palette mode
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"
        output = BytesIO()
        img.save(output, format="JPEG", quality=85, optimize=True)
        output.seek(0)

    return output.read(), filename


def _upload_to_s3(file_bytes: bytes, key: str) -> None:
    s3 = _get_s3_client()
    s3.upload_fileobj(
        BytesIO(file_bytes),
        settings.S3_BUCKET_NAME,
        key,
        ExtraArgs={"ContentType": "image/jpeg"},
    )


def _delete_from_s3(key: str) -> None:
    logger.debug(f"_delete_from_s3 called with key: {key}")
    s3 = _get_s3_client()
    logger.debug(f"S3 client created. Bucket: {settings.S3_BUCKET_NAME}")
    response = s3.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
    logger.debug(f"S3 delete_object response: {response}")


async def upload_profile_picture_to_s3(file_bytes: bytes, filename: str) -> None:
    key = f"profile_pics/{filename}"
    await run_in_threadpool(_upload_to_s3, file_bytes, key)


async def delete_profile_picture_from_s3(filename: str) -> None:
    logger.info(f"delete_profile_picture_from_s3 called with filename: {filename}")
    if not filename:
        logger.warning("Empty filename provided to delete_profile_picture_from_s3")
        return

    key = f"profile_pics/{filename}"
    logger.info(f"Constructed S3 key: {key}")
    await run_in_threadpool(_delete_from_s3, key)
