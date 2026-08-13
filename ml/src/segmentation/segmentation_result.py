"""
HemoVision — Segmentation Result Data Model
Container for palpebral conjunctiva detection and segmentation outputs.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Tuple
import numpy as np


@dataclass
class SegmentationResult:
    """Dataclass holding outputs from conjunctiva detection and segmentation."""

    success: bool
    mask: np.ndarray  # Binary uint8 mask [H, W], values in {0, 255}
    bounding_box: Tuple[int, int, int, int]  # (x, y, width, height)
    roi_image: np.ndarray  # Cropped RGB ROI image [H_roi, W_roi, 3]
    roi_area_pixels: int
    roi_area_ratio: float  # Fraction of total image area
    segmentation_quality: float  # Algorithmic quality score in [0.0, 1.0]
    failure_reason: Optional[str] = None
    method: str = "classical_cv"
    quality_flags: Dict[str, bool] = field(default_factory=dict)
    processing_time_ms: float = 0.0
    visual_overlay: Optional[np.ndarray] = None

    @property
    def confidence(self) -> Optional[float]:
        """Alias for algorithmic segmentation quality score."""
        return self.segmentation_quality if self.success else None

    @property
    def roi_crop(self) -> np.ndarray:
        """Backward compatibility alias for roi_image."""
        return self.roi_image

    @property
    def coverage_ratio(self) -> float:
        """Backward compatibility alias for roi_area_ratio."""
        return self.roi_area_ratio

    @property
    def quality_metrics(self) -> Dict[str, float]:
        """Backward compatibility dictionary for quality metrics."""
        return {
            "roi_area_pixels": float(self.roi_area_pixels),
            "coverage_ratio": float(self.roi_area_ratio),
            "segmentation_quality": float(self.segmentation_quality),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize metadata (excluding large numpy arrays) to dict."""
        return {
            "success": self.success,
            "method": self.method,
            "bounding_box": list(self.bounding_box),
            "roi_area_pixels": self.roi_area_pixels,
            "roi_area_ratio": round(self.roi_area_ratio, 4),
            "segmentation_quality": round(self.segmentation_quality, 4) if self.segmentation_quality is not None else None,
            "confidence": round(self.confidence, 4) if self.confidence is not None else None,
            "failure_reason": self.failure_reason,
            "quality_flags": self.quality_flags,
            "processing_time_ms": round(self.processing_time_ms, 2),
        }
