"""
HemoVision — Clinical & Synthetic Dataset Import CLI
Usage: python -m ml.src.data.import_dataset --input dataset/samples --output dataset/clinical --dry-run
"""

import argparse
from pathlib import Path
import json
import shutil

from ml.src.data.governance_gate import GovernanceGate, GovernanceState
from ml.src.data.dataset_loader import DatasetLoader
from ml.src.data.dataset_validator import DatasetValidator
from ml.src.data.image_hash import ImageHasher
from ml.src.data.exif_sanitizer import EXIFSanitizer
from ml.src.data.lab_alignment import LabAligner
from ml.src.data.withdrawal import WithdrawalManager
from ml.src.data.dataset_version import DatasetVersionManager
from ml.src.quality.quality_assessment import ResearchQualityAssessor
from ml.src.segmentation.conjunctiva_segmenter import create_segmenter


def run_import_dataset(input_dir: str, output_dir: str, dry_run: bool = False):
    in_path = Path(input_dir)
    out_path = Path(output_dir)

    print("============================================================")
    print("HemoVision Research Dataset Importer")
    print("============================================================")
    print(f"Input Location:  {in_path.resolve()}")
    print(f"Output Location: {out_path.resolve()}")
    print(f"Dry Run Mode:    {dry_run}\n")

    # 1. Evaluate Governance Gate
    gate = GovernanceGate(str(in_path))
    gov_res = gate.evaluate()

    print(f"[Governance Gate] Classification: {gov_res.state.value}")
    print(f"[Governance Gate] Clinical Training Allowed: {gov_res.is_clinical_training_allowed}")
    if gov_res.rejection_reasons:
        print("[Governance Gate] Governance Notes/Rejections:")
        for r in gov_res.rejection_reasons:
            print(f"  - {r}")
    print()

    # 2. Discover & Load Records
    loader = DatasetLoader(str(in_path))
    records = loader.load_records()
    print(f"[Dataset Loader] Loaded {len(records)} image/session records.")

    # 3. Quality & Segmentation Evaluation
    quality_assessor = ResearchQualityAssessor()
    segmenter = create_segmenter("classical_cv")

    usable_count = 0
    seg_success_count = 0

    for r in records:
        if r.image_path:
            img_p = in_path / r.image_path
            if not img_p.exists() and Path(r.image_path).exists():
                img_p = Path(r.image_path)
            if img_p.exists():
                import cv2
                bgr = cv2.imread(str(img_p))
                if bgr is not None:
                    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                    q_res = quality_assessor.assess(rgb)
                    if q_res.is_usable:
                        usable_count += 1
                    s_res = segmenter.segment(rgb)
                    if s_res.success:
                        seg_success_count += 1

    print(f"[Quality Gate] Usable Images: {usable_count}/{len(records)}")
    print(f"[Segmentation Engine] Segmented ROIs: {seg_success_count}/{len(records)}")

    # 4. Generate Quality Dashboard Report
    dashboard = {
        "dataset_type": gov_res.state.value,
        "governance_status": gov_res.metadata.get("governance_status", "unverified"),
        "clinical_training_allowed": gov_res.is_clinical_training_allowed,
        "total_records": len(records),
        "total_participants": len(set(r.participant_id for r in records)),
        "usable_images": usable_count,
        "rejected_images": len(records) - usable_count,
        "segmentation_successes": seg_success_count,
        "dry_run": dry_run,
    }

    if not dry_run:
        out_path.mkdir(parents=True, exist_ok=True)
        with open(out_path / "dataset_quality_dashboard.json", "w", encoding="utf-8") as f:
            json.dump(dashboard, f, indent=2)

        ver_mgr = DatasetVersionManager(version="1.0.0", dataset_type=gov_res.state.value.lower())
        ver_mgr.create_manifest(
            governance_status=gov_res.metadata.get("governance_status", "unverified"),
            total_participants=len(set(r.participant_id for r in records)),
            total_sessions=len(set(r.session_id for r in records)),
            total_images=len(records),
            usable_images=usable_count,
            excluded_images=len(records) - usable_count,
            withdrawn_participants=0,
            train_count=len(records),
            val_count=0,
            test_count=0,
            output_path=str(out_path / "dataset_manifest.json")
        )

    print("\n============================================================")
    if dry_run:
        print("[HemoVision] DRY RUN COMPLETE. No files were written to clinical destination.")
    else:
        print(f"[HemoVision] Import complete. Manifest and quality dashboard saved to {out_path}")
    print("============================================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HemoVision Clinical Research Dataset Importer")
    parser.add_argument("--input", type=str, default="dataset/samples", help="Input dataset directory")
    parser.add_argument("--output", type=str, default="dataset/clinical", help="Output dataset destination")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report without modifying disk")
    args = parser.parse_args()

    run_import_dataset(args.input, args.output, dry_run=args.dry-run if hasattr(args, 'dry-run') else args.dry_run)
