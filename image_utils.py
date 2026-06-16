import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

PROFILE_PICS_DIR = Path("media/profile_pics")


def process_profile_picture(content: bytes) -> str:
    with Image.open(BytesIO(content)) as original:
        # Correct orientation based on EXIF data and resize to 300x300 while maintaining aspect ratio
        img = ImageOps.exif_transpose(original)
        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        # Convert to RGB if the image has an alpha channel or is in palette mode
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        # Generate a unique filename and save the processed image
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = PROFILE_PICS_DIR / filename

        PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)

        img.save(file_path, format="JPEG", quality=85, optimize=True)

        return filename


def delete_profile_picture(filename: str | None) -> None:
    if filename is None:
        return

    file_path = PROFILE_PICS_DIR / filename
    if file_path.exists():
        file_path.unlink()
