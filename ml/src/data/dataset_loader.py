"""
HemoVision Dataset Loader
Loads Phase 1 entities (Participant, Session, Image, Lab Measurement, Annotation) into a unified ML representation.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json


@dataclass
class DatasetRecord:
    participant_id: str
    session_id: str
    image_id: str
    lab_measurement_id: str
    image_path: str
    laboratory_hb_g_dl: Optional[float]
    eye_side: str
    camera_lens_direction: str
    camera_lens_type: str
    phone_manufacturer: str
    phone_model: str
    lighting_condition: str
    capture_environment: str
    quality_status: str
    focus_score: float
    age: Optional[int] = None
    sex: Optional[str] = None
    annotation_mask_path: Optional[str] = None


class DatasetLoader:
    """Loads entity JSON files from dataset directory into structured DatasetRecord objects."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.samples_dir = self.root_dir / "samples"
        self.metadata_dir = self.root_dir / "metadata"

    def load_records(self) -> List[DatasetRecord]:
        records: List[DatasetRecord] = []
        
        # Look for entity JSON files in samples or metadata subdirectories
        search_dirs = [self.samples_dir, self.metadata_dir, self.root_dir]
        
        participants_data = self._find_and_load(search_dirs, ["participants.json", "participant.example.json", "participants.jsonl"])
        sessions_data = self._find_and_load(search_dirs, ["sessions.json", "session.example.json", "sessions.jsonl"])
        images_data = self._find_and_load(search_dirs, ["images.json", "image.example.json", "images.jsonl"])
        labs_data = self._find_and_load(search_dirs, ["lab_measurements.json", "lab_measurement.example.json", "lab_measurements.jsonl"])
        annotations_data = self._find_and_load(search_dirs, ["annotations.json", "annotation.example.json", "annotations.jsonl"])

        # Create dictionaries for fast lookup
        labs_by_participant: Dict[str, Dict] = {}
        for lab in labs_data:
            pid = lab.get("participant_id")
            if pid:
                labs_by_participant[pid] = lab

        participants_by_id: Dict[str, Dict] = {}
        for p in participants_data:
            pid = p.get("participant_id")
            if pid:
                participants_by_id[pid] = p

        sessions_by_id: Dict[str, Dict] = {}
        for s in sessions_data:
            sid = s.get("session_id")
            if sid:
                sessions_by_id[sid] = s

        annotations_by_image: Dict[str, Dict] = {}
        for ann in annotations_data:
            iid = ann.get("image_id")
            if iid:
                annotations_by_image[iid] = ann

        for img in images_data:
            image_id = img.get("image_id", "UNKNOWN")
            session_id = img.get("session_id", "UNKNOWN")
            participant_id = img.get("participant_id", "UNKNOWN")

            session = sessions_by_id.get(session_id, {})
            participant = participants_by_id.get(participant_id, {})
            lab = labs_by_participant.get(participant_id, {})
            ann = annotations_by_image.get(image_id, {})

            lab_hb = lab.get("hemoglobin_g_dl") or lab.get("laboratory_hb_g_dl")
            
            record = DatasetRecord(
                participant_id=participant_id,
                session_id=session_id,
                image_id=image_id,
                lab_measurement_id=lab.get("lab_measurement_id", "UNKNOWN"),
                image_path=img.get("image_path", ""),
                laboratory_hb_g_dl=float(lab_hb) if lab_hb is not None else None,
                eye_side=img.get("eye_side", "unknown"),
                camera_lens_direction=img.get("camera_lens_direction", "unknown"),
                camera_lens_type=img.get("camera_lens_type", "unknown"),
                phone_manufacturer=img.get("phone_manufacturer", "unknown"),
                phone_model=img.get("phone_model", "unknown"),
                lighting_condition=session.get("lighting_condition", img.get("lighting_condition", "unknown")),
                capture_environment=session.get("capture_environment", img.get("capture_environment", "unknown")),
                quality_status=img.get("image_quality_status", "usable"),
                focus_score=float(img.get("focus_score", 150.0)),
                age=participant.get("age_years"),
                sex=participant.get("biological_sex"),
                annotation_mask_path=ann.get("mask_path"),
            )
            records.append(record)

        return records

    def _find_and_load(self, search_dirs: List[Path], filenames: List[str]) -> List[Dict]:
        for sdir in search_dirs:
            if not sdir.exists():
                continue
            for fname in filenames:
                fpath = sdir / fname
                if fpath.exists():
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            content = json.load(f)
                            if isinstance(content, list):
                                return content
                            elif isinstance(content, dict):
                                return [content]
                    except Exception:
                        pass
        return []
