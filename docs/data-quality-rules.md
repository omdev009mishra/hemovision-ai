# Dataset Quality Rules & Validation Framework

This document defines the 7 deterministic data quality rules enforced during dataset ingestion and CI/CD validation.

---

## 1. Quality Rule Definitions

### Rule 1 — Participant Identity Uniqueness
* **Requirement**: No duplicate `participant_id` keys allowed in participant metadata tables.
* **Violation Check**: Duplicate participant ID detection triggers immediate ingestion failure.

### Rule 2 — Referential Integrity
* **Requirement**: Every `session_id` must reference a valid `participant_id`. Every `image_id` must reference a valid `session_id` and `participant_id`. Every `annotation_id` must reference a valid `image_id`. Every `lab_measurement_id` must reference a valid `participant_id`.
* **Violation Check**: Orphaned image, session, lab, or annotation records are rejected.

### Rule 3 — Laboratory Linkage Verification
* **Requirement**: Every training image must be linked to a valid laboratory reference measurement (`lab_quality_status == "valid_verified"`) for the same `participant_id`.
* **Violation Check**: Training images lacking valid reference lab measurements are flagged as unusable for supervised model training.

### Rule 4 — Timestamp Consistency & Format
* **Requirement**: All timestamps (`session_timestamp`, `capture_timestamp`, `measurement_timestamp`) must be valid ISO 8601 formatted UTC strings.
* **Violation Check**: Invalid timestamp strings or malformed date-times are rejected.

### Rule 5 — Image Quality Gate Enforcement
* **Requirement**: Images marked with quality rejection status (`rejected_blur`, `rejected_exposure`, `rejected_occlusion`, `rejected_framing`) MUST NOT silently enter model training or evaluation splits.
* **Violation Check**: Pipeline verifies that `image_quality_status == "usable"` for all training samples.

### Rule 6 — Zero Participant Leakage
* **Requirement**: No `participant_id` may exist in more than one dataset split (`train`, `validation`, `test`).
* **Violation Check**: Set intersection of participant IDs across splits MUST be empty:
  $$\text{Train Participants} \cap \text{Validation Participants} = \emptyset$$
  $$\text{Train Participants} \cap \text{Test Participants} = \emptyset$$

### Rule 7 — Explicit Missingness Representation
* **Requirement**: Missing optional attributes must be represented using explicit nulls, allowed unknown enumerations (`"unknown"`), or empty arrays (`[]`), rather than silent imputation or undefined keys.
* **Violation Check**: Schema validation fails on unmapped keys.
