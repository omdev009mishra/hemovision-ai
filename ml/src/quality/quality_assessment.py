"""
HemoVision — Phase 4: Image Quality Assessment Engine

Implements Laplacian focus blur variance, luminance over/underexposure ratios,
specular highlight detection, and overall engineering quality score computation [0, 1].

NOTE: Quality scores are engineering heuristics designed for dataset filtering and
user guidance. They do NOT represent medical confidence or diagnostic reliability.
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple
import numpy as np


@dataclass
class QualityAssessmentResult:
    """Container for research image quality assessment metrics."""
    quality_score: float  # Composite quality score in range [0.0, 1.0]
    is_usable: bool  # True if all quality thresholds are satisfied
    focus_score: float  # Laplacian variance
    mean_intensity: float  # Luminance mean in [0, 255]
    overexposure_ratio: float  # Fraction of pixels > 240
    underexposure_ratio: float  # Fraction of pixels < 15
    specular_ratio: float  # Glare pixel ratio > 250
    rejection_reasons: Tuple[str, ...]  # Tuple of rejection labels if unusable


def calculate_laplacian_variance(image_gray: np.ndarray) -> float:
    """
    Compute focus score using 3x3 discrete Laplacian operator variance.
    Kernel: [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
    """
    if image_gray.ndim != 2:
        raise ValueError("Input image must be a 2D grayscale array.")

    # 3x3 Laplacian convolution via numpy
    padded = np.pad(image_gray.astype(np.float64), 1, mode='edge')
    laplacian = (
        padded[1:-1, 2:] + padded[1:-1, :-2] +
        padded[2:, 1:-1] + padded[:-2, 1:-1] -
        4.0 * padded[1:-1, 1:-1]
    )
    return float(np.var(laplacian))


class ResearchQualityAssessor:
    """
    Quality Gating engine evaluating focus, luminance, specularity, and ROI visibility.
    """

    def __init__(
        self,
        min_focus_score: float = 100.0,
        max_overexposure_ratio: float = 0.15,
        max_underexposure_ratio: float = 0.15,
        max_specular_ratio: float = 0.08,
        optimal_luminance_center: float = 128.0,
    ):
        self.min_focus_score = min_focus_score
        self.max_overexposure_ratio = max_overexposure_ratio
        self.max_underexposure_ratio = max_underexposure_ratio
        self.max_specular_ratio = max_specular_ratio
        self.optimal_luminance_center = optimal_luminance_center

    def assess(self, image_rgb: np.ndarray) -> QualityAssessmentResult:
        """
        Assess an RGB image array.

        Args:
            image_rgb: RGB uint8 numpy array [H, W, 3]

        Returns:
            QualityAssessmentResult object containing quality metrics and usability flag.
        """
        if image_rgb is None or image_rgb.size == 0 or len(image_rgb.shape) != 3:
            raise ValueError("Input image must be a non-empty 3-channel uint8 array.")

        # Convert RGB to Grayscale for focus and luminance analysis
        gray = (
            0.299 * image_rgb[:, :, 0] +
            0.587 * image_rgb[:, :, 1] +
            0.114 * image_rgb[:, :, 2]
        ).astype(np.uint8)

        total_pixels = gray.size

        # 1. Focus Score (Laplacian Variance)
        focus_score = calculate_laplacian_variance(gray)

        # 2. Exposure Metrics
        mean_intensity = float(np.mean(gray))
        overexposed_ratio = float(np.sum(gray > 240) / total_pixels)
        underexposed_ratio = float(np.sum(gray < 15) / total_pixels)

        # 3. Specular Highlight Ratio
        specular_ratio = float(np.sum(gray > 250) / total_pixels)

        # 4. Evaluate Rejection Criteria
        rejection_reasons = []

        if focus_score < self.min_focus_score:
            rejection_reasons.append("rejected_blur")

        if overexposed_ratio > self.max_overexposure_ratio:
            rejection_reasons.append("rejected_overexposure")

        if underexposed_ratio > self.max_underexposure_ratio:
            rejection_reasons.append("rejected_underexposure")

        if specular_ratio > self.max_specular_ratio:
            rejection_reasons.append("rejected_specularity")

        is_usable = (len(rejection_reasons) == 0)

        # 5. Aggregate Engineering Quality Score [0.0, 1.0]
        # Focus component (capped at 500)
        norm_focus = min(focus_score / 500.0, 1.0)
        # Luminance deviation component from ideal center 128
        lum_dev = abs(mean_intensity - self.optimal_luminance_center) / 128.0
        norm_lum = max(1.0 - lum_dev, 0.0)
        # Over/under penalty
        exposure_penalty = max(1.0 - (overexposed_ratio + underexposed_ratio), 0.0)

        quality_score = float(0.4 * norm_focus + 0.3 * norm_lum + 0.3 * exposure_penalty)
        quality_score = max(0.0, min(1.0, quality_score))

        return QualityAssessmentResult(
            quality_score=quality_score,
            is_usable=is_usable,
            focus_score=focus_score,
            mean_intensity=mean_intensity,
            overexposure_ratio=overexposed_ratio,
            underexposure_ratio=underexposed_ratio,
            specular_ratio=specular_ratio,
            rejection_reasons=tuple(rejection_reasons),
        )
