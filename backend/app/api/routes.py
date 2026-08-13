"""
HemoVision API Router — Endpoints definition
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from typing import Optional, Dict, Any
import uuid
import datetime

from backend.app.api.schemas import (
    HealthResponse,
    AnalysisResponse,
    ImageAnalysisPayload,
    QualitySummary,
    SegmentationSummary,
    PredictionSummary,
    DemoPresetsResponse,
)
from backend.app.services.inference_service import InferenceService
from backend.app.services.report_service import ReportService
from backend.app.services.preset_service import PresetService

router = APIRouter(prefix="/api/v1", tags=["HemoVision API"])
inference_service = InferenceService()


@router.get("/health", response_model=HealthResponse)
def get_health():
    """System health check and safety boundary status."""
    return HealthResponse()


@router.get("/demo-samples", response_model=DemoPresetsResponse)
def get_demo_samples():
    """Retrieve 1-click synthetic demo presets for live judge testing."""
    return DemoPresetsResponse(presets=PresetService.get_presets())


def _format_analysis_response(result) -> AnalysisResponse:
    session_id = f"HV-SESS-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    quality_summary = QualitySummary(
        is_usable=result.is_usable,
        quality_score=round(result.quality_score, 2),
        rejection_reasons=list(result.rejection_reasons),
        focus_score=round(result.quality_details.get("focus_score", 0.0), 1),
        mean_intensity=round(result.quality_details.get("mean_intensity", 0.0), 1),
        overexposure_ratio=round(result.quality_details.get("overexposure_ratio", 0.0), 3),
        underexposure_ratio=round(result.quality_details.get("underexposure_ratio", 0.0), 3),
        specular_ratio=round(result.quality_details.get("specular_ratio", 0.0), 3),
    )

    segmentation_summary = SegmentationSummary(
        roi_area_pixels=result.segmentation_details.get("roi_area_pixels", 0.0),
        coverage_ratio=round(result.segmentation_details.get("coverage_ratio", 0.0), 4),
        aspect_ratio=round(result.segmentation_details.get("aspect_ratio", 0.0), 2),
        compactness=round(result.segmentation_details.get("compactness", 0.0), 3),
    )

    prediction_summary = PredictionSummary(
        estimated_hb_g_dl=result.estimated_hb_g_dl,
        prediction_interval=list(result.prediction_interval) if result.prediction_interval else None,
        confidence_level=result.confidence_level,
        reliability_score=result.reliability_score,
        research_category=result.research_category,
    )

    return AnalysisResponse(
        session_id=session_id,
        timestamp=timestamp,
        is_usable=result.is_usable,
        quality=quality_summary,
        segmentation=segmentation_summary,
        features=result.feature_summary,
        prediction=prediction_summary,
        disclaimer=result.disclaimer,
        visual_overlay_b64=result.visual_overlay_b64,
        roi_crop_b64=result.roi_crop_b64,
    )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image_json(payload: ImageAnalysisPayload):
    """Analyze conjunctival image base64 JSON payload."""
    try:
        result = inference_service.analyze_b64(payload.image_b64)
        return _format_analysis_response(result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal inference failure: {str(e)}")


@router.post("/analyze/file", response_model=AnalysisResponse)
async def analyze_image_file(file: UploadFile = File(...)):
    """Analyze uploaded conjunctival image binary file."""
    try:
        image_bytes = await file.read()
        result = inference_service.analyze_bytes(image_bytes)
        return _format_analysis_response(result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal inference failure: {str(e)}")


@router.post("/reports/markdown")
async def generate_markdown_report(payload: ImageAnalysisPayload):
    """Generate Markdown research summary report for session."""
    result = inference_service.analyze_b64(payload.image_b64)
    session_id = f"HV-SESS-{uuid.uuid4().hex[:8].upper()}"
    markdown_content = ReportService.generate_markdown_report(session_id, result)
    return {"session_id": session_id, "markdown": markdown_content}
