"""
HemoVision — Image SHA-256 Hashing Engine
Computes cryptographic SHA-256 hashes for imported research images for duplicate detection and integrity tracking.
"""

from pathlib import Path
from typing import Union
import hashlib


class ImageHasher:
    """Computes SHA-256 checksums for image files and byte buffers."""

    @staticmethod
    def hash_file(file_path: Union[str, Path]) -> str:
        """Computes SHA-256 hex digest of a local image file."""
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Image file not found for hashing: {file_path}")

        sha256 = hashlib.sha256()
        with open(p, "rb") as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def hash_bytes(image_bytes: bytes) -> str:
        """Computes SHA-256 hex digest of an in-memory byte buffer."""
        return hashlib.sha256(image_bytes).hexdigest()
