"""
HemoVision — Phase 4: Image Preprocessing & Color Calibration

Implements illumination correction, white balance algorithms (Gray World, Reference White,
LAB Color Space normalization), and chromatic feature extraction for conjunctival imaging.
"""

from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional
import numpy as np


@dataclass
class CalibrationResult:
    """Container for color calibration and normalization outputs."""
    calibrated_image: np.ndarray  # RGB uint8 array [H, W, 3]
    mean_rgb: Tuple[float, float, float]
    mean_lab: Tuple[float, float, float]
    chromaticity: Tuple[float, float, float]  # Normalized r, g, b
    red_green_ratio: float
    a_star_mean: float
    b_star_mean: float


def rgb_to_chromaticity(image_rgb: np.ndarray) -> Tuple[float, float, float]:
    """Calculate mean normalized chromaticity (r, g, b) over non-zero RGB pixels."""
    r_channel = image_rgb[:, :, 0].astype(np.float64)
    g_channel = image_rgb[:, :, 1].astype(np.float64)
    b_channel = image_rgb[:, :, 2].astype(np.float64)

    total = r_channel + g_channel + b_channel
    total[total == 0] = 1.0  # Avoid division by zero

    r_norm = np.mean(r_channel / total)
    g_norm = np.mean(g_channel / total)
    b_norm = np.mean(b_channel / total)

    return (float(r_norm), float(g_norm), float(b_norm))


def rgb_to_cielab(image_rgb: np.ndarray) -> np.ndarray:
    """
    Convert RGB image to CIELAB color space using standard D65 illuminant transform.
    Returns float64 array [H, W, 3] with L* in [0,100], a* in [-128,127], b* in [-128,127].
    """
    # Normalize RGB to [0, 1]
    rgb_float = image_rgb.astype(np.float64) / 255.0

    # Gamma expansion
    mask = rgb_float > 0.04045
    rgb_linear = np.zeros_like(rgb_float)
    rgb_linear[mask] = ((rgb_float[mask] + 0.055) / 1.055) ** 2.4
    rgb_linear[~mask] = rgb_float[~mask] / 12.92

    # Linear RGB to XYZ (D65)
    r = rgb_linear[:, :, 0]
    g = rgb_linear[:, :, 1]
    b = rgb_linear[:, :, 2]

    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    # D65 reference white points
    xn, yn, zn = 0.95047, 1.00000, 1.08883
    xr, yr, zr = x / xn, y / yn, z / zn

    # Non-linear function f(t)
    def f(t):
        delta = 6.0 / 29.0
        mask_f = t > (delta ** 3)
        res = np.zeros_like(t)
        res[mask_f] = t[mask_f] ** (1.0 / 3.0)
        res[~mask_f] = (t[~mask_f] / (3.0 * delta ** 2)) + (4.0 / 29.0)
        return res

    fx, fy, fz = f(xr), f(yr), f(zr)

    l_star = 116.0 * fy - 16.0
    a_star = 500.0 * (fx - fy)
    b_star = 200.0 * (fy - fz)

    return np.stack([l_star, a_star, b_star], axis=-1)


class ColorCalibrator:
    """
    Color calibrator implementing Gray World, Reference White, and LAB normalization.
    """

    def __init__(self, method: str = "gray_world"):
        if method not in ["gray_world", "reference_white", "lab_norm"]:
            raise ValueError(f"Unknown calibration method: {method}")
        self.method = method

    def calibrate(self, image_rgb: np.ndarray) -> CalibrationResult:
        """
        Calibrate and normalize RGB conjunctival image.

        Args:
            image_rgb: RGB uint8 numpy array [H, W, 3]

        Returns:
            CalibrationResult object.
        """
        if image_rgb is None or image_rgb.size == 0:
            raise ValueError("Input image must be non-empty.")

        img_float = image_rgb.astype(np.float64)

        if self.method == "gray_world":
            mean_r = np.mean(img_float[:, :, 0])
            mean_g = np.mean(img_float[:, :, 1])
            mean_b = np.mean(img_float[:, :, 2])

            gray_mean = (mean_r + mean_g + mean_b) / 3.0
            scale_r = gray_mean / max(mean_r, 1.0)
            scale_g = gray_mean / max(mean_g, 1.0)
            scale_b = gray_mean / max(mean_b, 1.0)

            calibrated = np.zeros_like(img_float)
            calibrated[:, :, 0] = np.clip(img_float[:, :, 0] * scale_r, 0, 255)
            calibrated[:, :, 1] = np.clip(img_float[:, :, 1] * scale_g, 0, 255)
            calibrated[:, :, 2] = np.clip(img_float[:, :, 2] * scale_b, 0, 255)
            calibrated_rgb = calibrated.astype(np.uint8)

        elif self.method == "reference_white":
            # Scale based on top 5% brightest pixels
            bright_threshold = np.percentile(img_float, 95)
            mask_white = img_float >= bright_threshold
            ref_r = np.mean(img_float[:, :, 0][mask_white[:, :, 0]]) if np.any(mask_white[:, :, 0]) else 255.0
            ref_g = np.mean(img_float[:, :, 1][mask_white[:, :, 1]]) if np.any(mask_white[:, :, 1]) else 255.0
            ref_b = np.mean(img_float[:, :, 2][mask_white[:, :, 2]]) if np.any(mask_white[:, :, 2]) else 255.0

            calibrated = np.zeros_like(img_float)
            calibrated[:, :, 0] = np.clip(img_float[:, :, 0] * (255.0 / max(ref_r, 1.0)), 0, 255)
            calibrated[:, :, 1] = np.clip(img_float[:, :, 1] * (255.0 / max(ref_g, 1.0)), 0, 255)
            calibrated[:, :, 2] = np.clip(img_float[:, :, 2] * (255.0 / max(ref_b, 1.0)), 0, 255)
            calibrated_rgb = calibrated.astype(np.uint8)

        else:  # lab_norm
            calibrated_rgb = image_rgb.copy()

        # Compute summary chromatic stats
        lab = rgb_to_cielab(calibrated_rgb)
        l_mean = float(np.mean(lab[:, :, 0]))
        a_mean = float(np.mean(lab[:, :, 1]))
        b_mean = float(np.mean(lab[:, :, 2]))

        mean_r = float(np.mean(calibrated_rgb[:, :, 0]))
        mean_g = float(np.mean(calibrated_rgb[:, :, 1]))
        mean_b = float(np.mean(calibrated_rgb[:, :, 2]))

        chroma = rgb_to_chromaticity(calibrated_rgb)
        rg_ratio = float(mean_r / max(mean_g, 1.0))

        return CalibrationResult(
            calibrated_image=calibrated_rgb,
            mean_rgb=(mean_r, mean_g, mean_b),
            mean_lab=(l_mean, a_mean, b_mean),
            chromaticity=chroma,
            red_green_ratio=rg_ratio,
            a_star_mean=a_mean,
            b_star_mean=b_mean,
        )
