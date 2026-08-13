"""
HemoVision — Single Image Conjunctiva Segmentation CLI
Usage: python -m ml.src.segmentation.run_segmentation --image dataset/samples/segmentation/synthetic_eye_001.png --output research/results/segmentation/
"""

import argparse
from pathlib import Path
import json
import cv2

from ml.src.segmentation.conjunctiva_segmenter import create_segmenter
from ml.src.segmentation.visualization import SegmentationVisualizer


def run_single_image_segmentation(image_path: str, output_dir: str, config_path: str = "ml/configs/segmentation.yaml"):
    img_path = Path(image_path)
    if not img_path.exists():
        raise FileNotFoundError(f"Input image file not found: {image_path}")

    # Read RGB Image
    bgr = cv2.imread(str(img_path))
    if bgr is None:
        raise ValueError(f"Could not decode image at: {image_path}")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # Initialize Segmenter & Run Pipeline
    segmenter = create_segmenter("classical_cv", config_path=config_path)
    res = segmenter.segment(rgb)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save outputs
    # 1. segmentation_result.json
    result_dict = res.to_dict()
    result_dict["input_image"] = str(img_path)
    with open(out_dir / "segmentation_result.json", "w", encoding="utf-8") as f:
        json.dump(result_dict, f, indent=2)

    # 2. mask.png
    cv2.imwrite(str(out_dir / "mask.png"), res.mask)

    # 3. overlay.png
    overlay_rgb = res.visual_overlay if res.visual_overlay is not None else SegmentationVisualizer.create_overlay(rgb, res.mask, res.bounding_box)
    cv2.imwrite(str(out_dir / "overlay.png"), cv2.cvtColor(overlay_rgb, cv2.COLOR_RGB2BGR))

    # 4. roi.png
    cv2.imwrite(str(out_dir / "roi.png"), cv2.cvtColor(res.roi_image, cv2.COLOR_RGB2BGR))

    # 5. Diagnostic panel figure
    SegmentationVisualizer.save_diagnostic_panel(rgb, res, str(out_dir / "diagnostic_panel.png"))

    print(f"[HemoVision] Single image segmentation completed.")
    print(f"  - Status: {'SUCCESS' if res.success else 'FAILED'}")
    print(f"  - Method: {res.method}")
    print(f"  - ROI Area: {res.roi_area_pixels} px ({res.roi_area_ratio:.2%})")
    print(f"  - Processing Time: {res.processing_time_ms:.2f} ms")
    print(f"  - Output directory: {out_dir.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HemoVision Conjunctiva Single Image Segmentation CLI")
    parser.add_argument("--image", type=str, required=True, help="Path to input eye image")
    parser.add_argument("--output", type=str, default="research/results/segmentation/", help="Output directory")
    parser.add_argument("--config", type=str, default="ml/configs/segmentation.yaml", help="Path to segmentation config YAML")
    args = parser.parse_args()

    run_single_image_segmentation(args.image, args.output, args.config)
