"""
HemoVision — Conjunctiva Segmentation Benchmark CLI
Usage: python -m ml.src.segmentation.benchmark --dataset dataset/samples/segmentation --output research/results/segmentation/
"""

import argparse
from pathlib import Path
import json
import numpy as np
import pandas as pd
import cv2

from ml.src.segmentation.conjunctiva_segmenter import create_segmenter
from ml.src.evaluation.segmentation_metrics import calculate_segmentation_metrics


def run_benchmark(dataset_dir: str, output_dir: str, config_path: str = "ml/configs/segmentation.yaml"):
    ds_path = Path(dataset_dir)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    segmenter = create_segmenter("classical_cv", config_path=config_path)

    # Discover synthetic image fixtures
    image_files = sorted(list(ds_path.glob("*.png")) + list(ds_path.glob("*.jpg")))
    # Filter out ground-truth mask files ending in _mask.png
    image_files = [f for f in image_files if not f.name.endswith("_mask.png")]

    metrics_list = []
    runtimes = []
    success_count = 0

    for img_p in image_files:
        bgr = cv2.imread(str(img_p))
        if bgr is None:
            continue
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        res = segmenter.segment(rgb)
        runtimes.append(res.processing_time_ms)

        # Check for paired ground-truth mask
        mask_p = img_p.parent / f"{img_p.stem}_mask.png"
        has_gt = mask_p.exists()

        if has_gt:
            gt_mask = cv2.imread(str(mask_p), cv2.IMREAD_GRAYSCALE)
            eval_metrics = calculate_segmentation_metrics(res.mask, gt_mask)
        else:
            eval_metrics = {"iou": None, "dice": None, "precision": None, "recall": None, "pixel_accuracy": None}

        if res.success:
            success_count += 1

        metrics_list.append({
            "image_name": img_p.name,
            "success": res.success,
            "failure_reason": res.failure_reason or "",
            "roi_area_pixels": res.roi_area_pixels,
            "roi_area_ratio": round(res.roi_area_ratio, 4),
            "segmentation_quality": round(res.segmentation_quality, 4) if res.segmentation_quality is not None else None,
            "processing_time_ms": round(res.processing_time_ms, 2),
            "has_ground_truth": has_gt,
            "iou": eval_metrics["iou"],
            "dice": eval_metrics["dice"],
            "precision": eval_metrics["precision"],
            "recall": eval_metrics["recall"],
            "pixel_accuracy": eval_metrics["pixel_accuracy"],
        })

    # Save segmentation_metrics.csv
    df = pd.DataFrame(metrics_list)
    df.to_csv(out_dir / "segmentation_metrics.csv", index=False)

    total_images = len(image_files)

    # Compute aggregate stats for images with ground truth
    gt_df = df[df["has_ground_truth"] == True] if not df.empty else pd.DataFrame()
    mean_iou = float(gt_df["iou"].dropna().mean()) if not gt_df.empty and not gt_df["iou"].dropna().empty else None
    mean_dice = float(gt_df["dice"].dropna().mean()) if not gt_df.empty and not gt_df["dice"].dropna().empty else None
    mean_precision = float(gt_df["precision"].dropna().mean()) if not gt_df.empty and not gt_df["precision"].dropna().empty else None
    mean_recall = float(gt_df["recall"].dropna().mean()) if not gt_df.empty and not gt_df["recall"].dropna().empty else None
    median_runtime_ms = float(np.median(runtimes)) if runtimes else 0.0

    summary = {
        "dataset_type": "SYNTHETIC",
        "clinical_validation": "NOT PERFORMED",
        "total_images": total_images,
        "successful_segmentations": success_count,
        "failed_segmentations": total_images - success_count,
        "success_rate": round(success_count / total_images, 4) if total_images > 0 else 0.0,
        "mean_iou": round(mean_iou, 4) if mean_iou is not None else None,
        "mean_dice": round(mean_dice, 4) if mean_dice is not None else None,
        "mean_precision": round(mean_precision, 4) if mean_precision is not None else None,
        "mean_recall": round(mean_recall, 4) if mean_recall is not None else None,
        "median_processing_time_ms": round(median_runtime_ms, 2),
        "note": "SOFTWARE VALIDATION ONLY — NOT CLINICAL PERFORMANCE"
    }

    with open(out_dir / "benchmark_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Generate benchmark_report.md
    md = [
        "# HemoVision Conjunctiva Segmentation Benchmark Report",
        "",
        "## Governance Declaration",
        "- **Dataset Type**: `SYNTHETIC`",
        "- **Clinical Validation**: `NOT PERFORMED`",
        "- **Notice**: Software validation only. Synthetic fixture performance does not establish clinical accuracy.",
        "",
        "## Benchmark Summary",
        f"- **Total Images Evaluated**: {total_images}",
        f"- **Successful Segmentations**: {success_count}",
        f"- **Failed Segmentations**: {total_images - success_count}",
        f"- **Success Rate**: {summary['success_rate']:.2%}",
        f"- **Mean IoU**: {summary['mean_iou'] if summary['mean_iou'] is not None else 'N/A'}",
        f"- **Mean Dice Score**: {summary['mean_dice'] if summary['mean_dice'] is not None else 'N/A'}",
        f"- **Mean Precision**: {summary['mean_precision'] if summary['mean_precision'] is not None else 'N/A'}",
        f"- **Mean Recall**: {summary['mean_recall'] if summary['mean_recall'] is not None else 'N/A'}",
        f"- **Median Processing Time**: {summary['median_processing_time_ms']} ms",
        "",
    ]

    if total_images < 5:
        md.append("> **Note**: Insufficient data for meaningful statistical performance estimation.")
        md.append("")

    md.append("## Image Level Evaluation")
    for row in metrics_list:
        md.append(f"- **`{row['image_name']}`**: Success={row['success']} | Area={row['roi_area_pixels']}px ({row['roi_area_ratio']:.2%}) | Runtime={row['processing_time_ms']}ms | IoU={row['iou']} | Dice={row['dice']}")

    with open(out_dir / "benchmark_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"[HemoVision] Segmentation Benchmark complete.")
    print(f"  - Total Images: {total_images}")
    print(f"  - Success Rate: {summary['success_rate']:.2%}")
    print(f"  - Reports saved to: {out_dir.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HemoVision Conjunctiva Segmentation Benchmark")
    parser.add_argument("--dataset", type=str, default="dataset/samples/segmentation", help="Path to dataset directory")
    parser.add_argument("--output", type=str, default="research/results/segmentation/", help="Output directory")
    parser.add_argument("--config", type=str, default="ml/configs/segmentation.yaml", help="Path to segmentation config YAML")
    args = parser.parse_args()

    run_benchmark(args.dataset, args.output, args.config)
