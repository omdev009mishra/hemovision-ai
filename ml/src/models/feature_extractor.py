"""
HemoVision — Phase 6: Palpebral Conjunctiva Feature Extraction

Extracts 28 quantitative chromatic, morphological, and spectral proxy features
from segmented palpebral conjunctiva regions of interest (ROI).
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
import numpy as np
from ml.src.preprocessing.color_calibration import rgb_to_cielab


@dataclass
class FeatureVector:
    """Container for 28 extracted conjunctiva ROI features."""
    mean_r: float
    mean_g: float
    mean_b: float
    std_r: float
    std_g: float
    std_b: float
    r_chromaticity: float
    g_chromaticity: float
    b_chromaticity: float
    red_green_ratio: float
    red_blue_ratio: float
    redness_index: float  # (R - G) / (R + G)
    erythema_index: float  # log10(R) - log10(G)
    l_star_mean: float
    a_star_mean: float
    b_star_mean: float
    l_star_std: float
    a_star_std: float
    b_star_std: float
    hue_mean: float
    hue_std: float
    sat_mean: float
    sat_std: float
    val_mean: float
    val_std: float
    roi_area_pixels: float
    roi_aspect_ratio: float
    hb_absorption_proxy: float  # a* / (L* + 1.0)

    def to_array(self) -> np.ndarray:
        """Convert feature vector to 1D float64 numpy array."""
        return np.array(list(asdict(self).values()), dtype=np.float64)

    def to_dict(self) -> Dict[str, float]:
        """Convert feature vector to dictionary."""
        return asdict(self)

    @classmethod
    def feature_names(cls) -> List[str]:
        """List ordered feature names."""
        return list(cls.__annotations__.keys())


class FeatureExtractor:
    """
    Extracts chromaticity, CIELAB redness, HSV, and morphological features from ROI.
    """

    def extract(self, roi_rgb: np.ndarray, mask: Optional[np.ndarray] = None) -> FeatureVector:
        """
        Extract features from RGB ROI image and optional binary mask.

        Args:
            roi_rgb: RGB uint8 numpy array [H, W, 3]
            mask: Optional binary mask uint8 numpy array [H, W]

        Returns:
            FeatureVector object containing 28 extracted features.
        """
        if roi_rgb is None or roi_rgb.size == 0 or len(roi_rgb.shape) != 3:
            raise ValueError("Input ROI image must be a non-empty 3-channel uint8 array.")

        if mask is not None and mask.shape[:2] == roi_rgb.shape[:2] and np.any(mask > 0):
            valid_pixels = roi_rgb[mask > 0]
        else:
            valid_pixels = roi_rgb.reshape(-1, 3)

        r = valid_pixels[:, 0].astype(np.float64)
        g = valid_pixels[:, 1].astype(np.float64)
        b = valid_pixels[:, 2].astype(np.float64)

        mean_r, mean_g, mean_b = float(np.mean(r)), float(np.mean(g)), float(np.mean(b))
        std_r, std_g, std_b = float(np.std(r)), float(np.std(g)), float(np.std(b))

        total = mean_r + mean_g + mean_b
        total_denom = max(total, 1.0)
        r_chrom = mean_r / total_denom
        g_chrom = mean_g / total_denom
        b_chrom = mean_b / total_denom

        rg_ratio = mean_r / max(mean_g, 1.0)
        rb_ratio = mean_r / max(mean_b, 1.0)

        redness_index = (mean_r - mean_g) / max(mean_r + mean_g, 1.0)
        erythema_index = float(np.log10(max(mean_r, 1.0)) - np.log10(max(mean_g, 1.0)))

        # CIELAB calculation
        lab = rgb_to_cielab(roi_rgb)
        if mask is not None and mask.shape[:2] == roi_rgb.shape[:2] and np.any(mask > 0):
            valid_lab = lab[mask > 0]
        else:
            valid_lab = lab.reshape(-1, 3)

        l_star, a_star, b_star = valid_lab[:, 0], valid_lab[:, 1], valid_lab[:, 2]
        l_mean, a_mean, b_mean = float(np.mean(l_star)), float(np.mean(a_star)), float(np.mean(b_star))
        l_std, a_std, b_std = float(np.std(l_star)), float(np.std(a_star)), float(np.std(b_star))

        # HSV calculation
        import cv2
        hsv = cv2.cvtColor(roi_rgb, cv2.COLOR_RGB2HSV)
        if mask is not None and mask.shape[:2] == roi_rgb.shape[:2] and np.any(mask > 0):
            valid_hsv = hsv[mask > 0]
        else:
            valid_hsv = hsv.reshape(-1, 3)

        h_val, s_val, v_val = valid_hsv[:, 0], valid_hsv[:, 1], valid_hsv[:, 2]
        hue_mean, hue_std = float(np.mean(h_val)), float(np.std(h_val))
        sat_mean, sat_std = float(np.mean(s_val)), float(np.std(s_val))
        val_mean, val_std = float(np.mean(v_val)), float(np.std(v_val))

        roi_area = float(valid_pixels.shape[0])
        h_dim, w_dim = roi_rgb.shape[:2]
        aspect_ratio = float(w_dim / max(h_dim, 1))

        hb_absorption_proxy = float(a_mean / (max(l_mean, 1.0) + 1.0))

        return FeatureVector(
            mean_r=mean_r,
            mean_g=mean_g,
            mean_b=mean_b,
            std_r=std_r,
            std_g=std_g,
            std_b=std_b,
            r_chromaticity=r_chrom,
            g_chromaticity=g_chrom,
            b_chromaticity=b_chrom,
            red_green_ratio=rg_ratio,
            red_blue_ratio=rb_ratio,
            redness_index=redness_index,
            erythema_index=erythema_index,
            l_star_mean=l_mean,
            a_star_mean=a_mean,
            b_star_mean=b_mean,
            l_star_std=l_std,
            a_star_std=a_std,
            b_star_std=b_std,
            hue_mean=hue_mean,
            hue_std=hue_std,
            sat_mean=sat_mean,
            sat_std=sat_std,
            val_mean=val_mean,
            val_std=val_std,
            roi_area_pixels=roi_area,
            roi_aspect_ratio=aspect_ratio,
            hb_absorption_proxy=hb_absorption_proxy,
        )
