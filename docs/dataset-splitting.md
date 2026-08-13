# Dataset Splitting & Semantic Versioning Protocol

This specification defines the participant-isolated dataset splitting rules and semantic versioning strategy for HemoVision.

---

## 1. 🛡️ Participant-Isolated Dataset Splitting

Dataset partitioning into **TRAIN**, **VALIDATION**, and **TEST** sets is governed by a strict isolation mandate:

> [!CAUTION]
> ### MANDATORY ISOLATION RULE
> **The PARTICIPANT ID is ALWAYS the atomic unit of dataset partitioning.**
> All sessions, images, and laboratory records associated with Participant A must reside EXCLUSIVELY within a single split (e.g. TRAIN). Participant A MUST NEVER appear across multiple splits under any circumstances, even if images were captured during different sessions or on different days.

### Partition Definitions
* **TRAIN SET (Approx. 70%)**: Used exclusively for model parameter optimization and loss minimization.
* **VALIDATION SET (Approx. 15%)**: Used for hyperparameter tuning, early stopping, and model selection.
* **TEST SET (Approx. 15%)**: Strictly held-out benchmark set. Evaluated ONLY once per formal dataset release to compute final unbiased clinical performance metrics.

---

## 2. Preventing Temporal & Subgroup Data Leakage

1. **Session & Multi-Frame Grouping**: All images from a single `session_id` or multi-frame burst are bound to their parent `participant_id` prior to split assignment.
2. **Temporal Isolation**: If longitudinal data collection spans multiple months, chronological partitioning (assigning earlier participants to TRAIN and later participants to TEST) must be evaluated to prevent temporal leakage across evolving software/hardware settings.
3. **Demographic & Device Stratification**: Random split generation must be stratified by key covariates (`sex`, `age_years` brackets, `skin_phototype`, `phone_manufacturer`, `anemia_label` distribution) to ensure balanced representation across TRAIN, VALIDATION, and TEST sets.

---

## 3. Semantic Dataset Versioning Scheme

Dataset releases follow a structured Semantic Versioning model (**`vMAJOR.MINOR.PATCH`**):

```text
vMAJOR.MINOR.PATCH
 │     │     └── PATCH: Fixes in metadata annotations, mask corrections, or schema updates.
 │     └─────── MINOR: Addition of new participant cohorts, sessions, or phone models.
 └───────────── MAJOR: Structural protocol changes, schema redesign, or new clinical trial phases.
```

### Dataset Version Manifest Specifications
Every compiled dataset release (e.g., `v0.1.0`) must produce an immutable version manifest JSON documenting:
* `dataset_version`: SemVer string (e.g. `v0.1.0`).
* `protocol_version`: Clinical collection protocol version SHA.
* `schema_version`: JSON Schema Draft 2020-12 version string.
* `split_creation_date`: ISO 8601 creation timestamp.
* `random_seed`: Deterministic seed used for pseudorandom split partitioning (e.g. `42`).
* `counts`: Total count of participants, sessions, images, laboratory reference measurements, and approved annotations.
* `split_manifest`: Mapping of `participant_id` to assigned split (`train`, `validation`, `test`).

> *Manifest JSON files record split assignments and metadata contracts. Raw clinical images and health data files remain stored in secure encrypted external storage and are NEVER committed to Git.*
