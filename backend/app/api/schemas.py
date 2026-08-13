"""
HemoVision API Schemas — Pydantic V2
Strict request and response models for FastAPI endpoints.
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="API operational status")
    version: str = Field(default="v1.0.0", description="API version")
    model_version: str = Field(default="hb-ridge-v1.0.0", description="ML model version")
    disclaimer: str = Field(
        default="HemoVision is an investigational research prototype. Not for medical diagnosis.",
        description="Medical safety disclaimer"
    )


class ImageAnalysisPayload(BaseModel):
    image_b64: str = Field(..., description="Base64 encoded image string")


class QualitySummary(BaseModel):
    is_usable: bool
    quality_score: float
    rejection_reasons: List[str]
    focus_score: float
    mean_intensity: float
    overexposure_ratio: float
    underexposure_ratio: float
    specular_ratio: float


class SegmentationSummary(BaseModel):
    roi_area_pixels: float
    coverage_ratio: float
    aspect_ratio: float
    compactness: float


class PredictionSummary(BaseModel):
    estimated_hb_g_dl: Optional[float]
    prediction_interval: Optional[List[float]]
    confidence_level: Optional[float]
    reliability_score: Optional[float]
    research_category: str


class AnalysisResponse(BaseModel):
    session_id: str
    timestamp: str
    is_usable: bool
    quality: QualitySummary
    segmentation: SegmentationSummary
    features: Dict[str, float]
    prediction: PredictionSummary
    disclaimer: str
    visual_overlay_b64: str
    roi_crop_b64: str


class PresetDemoSample(BaseModel):
    id: str
    name: str
    description: str
    expected_hb_g_dl: Optional[float]
    expected_status: str
    image_b64: str


class DemoPresetsResponse(BaseModel):
    presets: List[PresetDemoSample]
