# Dataset Specifications, Contracts & Schemas

This directory contains the authoritative JSON Schemas, synthetic testing fixtures, and metadata specifications for HemoVision.

---

## Entity Relationship Overview

```text
Participant
    │
    ├── Capture Session
    │       │
    │       ├── Left Eye Image ──> Segmentation Annotation
    │       ├── Right Eye Image ──> Segmentation Annotation
    │       └── Additional Frames
    │
    └── Laboratory Measurement (Hb Reference)
```

---

## Schema List (JSON Schema Draft 2020-12)

1. [`dataset/schema/participants.schema.json`](file:///d:/hemovision/dataset/schema/participants.schema.json) — Participant demographics, physiological state, and covariates.
2. [`dataset/schema/sessions.schema.json`](file:///d:/hemovision/dataset/schema/sessions.schema.json) — Capture session, device ID, operator ID, and environment metadata.
3. [`dataset/schema/images.schema.json`](file:///d:/hemovision/dataset/schema/images.schema.json) — Conjunctival photograph, hardware specs, focus/exposure scores, and quality status.
4. [`dataset/schema/lab_measurements.schema.json`](file:///d:/hemovision/dataset/schema/lab_measurements.schema.json) — Laboratory reference Hb measurement and instrument metadata.
5. [`dataset/schema/annotations.schema.json`](file:///d:/hemovision/dataset/schema/annotations.schema.json) — Palpebral conjunctiva segmentation mask annotation and review status.

---

## Synthetic Data Fixtures (`dataset/samples/`)

> [!WARNING]
> **Files under `dataset/samples/` are synthetic fictional examples used exclusively for schema testing. Real patient data must NEVER be stored in Git.**

* `participant.example.json`: Fictional participant record (`SYNTHETIC-P001`).
* `session.example.json`: Fictional capture session record (`SYNTHETIC-S001`).
* `image.example.json`: Fictional image record (`SYNTHETIC-IMG001`).
* `lab_measurement.example.json`: Fictional reference lab record (`SYNTHETIC-LAB001`).
* `annotation.example.json`: Fictional segmentation mask record (`SYNTHETIC-ANN001`).

---

## Data Privacy, Versioning & Validation Rules

* **Zero Patient Data in Git**: Raw clinical datasets and patient photographs are excluded via `.gitignore`.
* **Participant-Level Isolation**: TRAIN / VALIDATION / TEST partitioning **MUST** be performed at the `participant_id` level.
* **Semantic Versioning**: Releases follow SemVer (e.g. `v0.1.0`).
* **Validation**: Run deterministic metadata and schema validation locally using:
  ```bash
  python -m pytest ml/tests/ -v
  ```
