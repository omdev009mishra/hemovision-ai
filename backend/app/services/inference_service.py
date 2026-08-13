"""
HemoVision Backend Service — Inference Wrapper
"""

import base64
import numpy as np
import cv2
from ml.src.inference.pipeline import InferencePipeline, InferenceResult


class InferenceService:
    """Service wrapping ML InferencePipeline with image decoding helpers."""

    def __init__(self, model_path: str = None):
        self.pipeline = InferencePipeline(model_path=model_path)

    def analyze_bytes(self, image_bytes: bytes) -> InferenceResult:
        """Decode image bytes and process through ML pipeline."""
        if not image_bytes:
            raise ValueError("Image bytes must not be empty.")

        nparr = np.frombuffer(image_bytes, np.uint8)
        bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if bgr is None or bgr.size == 0:
            raise ValueError("Could not decode image from bytes.")

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return self.pipeline.process(rgb)

    def analyze_b64(self, image_b64: str) -> InferenceResult:
        """Decode base64 image string and process through ML pipeline."""
        if "," in image_b64:
            image_b64 = image_b64.split(",", 1)[1]

        image_bytes = base64.b64decode(image_b64)
        return self.analyze_bytes(image_bytes)
