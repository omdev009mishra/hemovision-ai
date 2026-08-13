"""
HemoVision — Image Ingestion & Validation Pipeline
Imports, validates file formats, computes checksums, sanitizes EXIF, and links image records.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import cv2

from ml.src.data.image_hash import ImageHasher
from ml.src.data.exif_sanitizer import EXIFSanitizer


@dataclass
class IngestedImageRecord:
    success: bool
    image_id: str
    session_id: str
    participant_id: str
    image_path: str
    sha256_hash: str
    width: int
    height: int
    sanitized_metadata: Dict[str, Any]
    failure_reason: Optional[str] = None


class ImageIngestor:
    """Validates and imports image files into the research data pipeline."""

    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def __init__(self, target_dir: str = "dataset/images"):
        self.target_dir = Path(target_dir)

    def ingest_image(
        self,
        source_path: str,
        session_id: str,
        participant_id: str,
        image_index: int = 0,
        raw_exif: Optional[Dict[str, Any]] = None
    ) -> IngestedImageRecord:
        src_p = Path(source_path)

        if not src_p.exists():
            return IngestedImageRecord(
                success=False,
                image_id="UNKNOWN",
                session_id=session_id,
                participant_id=participant_id,
                image_path=source_path,
                sha256_hash="",
                width=0,
                height=0,
                sanitized_metadata={},
                failure_reason=f"Source file does not exist: {source_path}"
            )

        ext = src_p.suffix.lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            return IngestedImageRecord(
                success=False,
                image_id="UNKNOWN",
                session_id=session_id,
                participant_id=participant_id,
                image_path=source_path,
                sha256_hash="",
                width=0,
                height=0,
                sanitized_metadata={},
                failure_reason=f"Unsupported image format '{ext}'. Must be JPEG or PNG."
            )

        # Decode image to verify readability
        bgr = cv2.imread(str(src_p))
        if bgr is None or bgr.size == 0:
            return IngestedImageRecord(
                success=False,
                image_id="UNKNOWN",
                session_id=session_id,
                participant_id=participant_id,
                image_path=source_path,
                sha256_hash="",
                width=0,
                height=0,
                sanitized_metadata={},
                failure_reason=f"Failed to decode image at: {source_path}"
            )

        h, w, _ = bgr.shape
        img_hash = ImageHasher.hash_file(src_p)
        sanitized_exif, _ = EXIFSanitizer.sanitize_metadata(raw_exif or {})

        image_id = f"HV-IMG-{img_hash[:8].upper()}"

        return IngestedImageRecord(
            success=True,
            image_id=image_id,
            session_id=session_id,
            participant_id=participant_id,
            image_path=str(src_p),
            sha256_hash=img_hash,
            width=w,
            height=h,
            sanitized_metadata=sanitized_exif,
            failure_reason=None
        )
