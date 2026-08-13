"""
Tests for ImageHasher
"""

import pytest
from ml.src.data.image_hash import ImageHasher


def test_image_hasher_bytes():
    data = b"synthetic_eye_image_data_buffer"
    h1 = ImageHasher.hash_bytes(data)
    h2 = ImageHasher.hash_bytes(data)

    assert len(h1) == 64  # SHA-256 hex length
    assert h1 == h2


def test_image_hasher_file(tmp_path):
    f_path = tmp_path / "test_img.png"
    f_path.write_bytes(b"sample_png_content_12345")

    h = ImageHasher.hash_file(f_path)
    assert len(h) == 64
