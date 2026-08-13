# HemoVision — Research Dataset Versioning Protocol

## 1. Semantic Versioning Scheme (`vMAJOR.MINOR.PATCH`)

Research dataset releases follow semantic versioning:

- **`MAJOR`**: Breaking changes to dataset schema, anatomical protocols, or governance requirements.
- **`MINOR`**: Ingestion of new participants, images, or validated clinical records.
- **`PATCH`**: Metadata corrections, documentation updates, or non-functional structural fixes.

---

## 2. Manifest Specifications (`dataset_manifest.json`)

Every versioned dataset release produces an immutable manifest declaring:
- `dataset_version`
- `dataset_type` (`synthetic` vs `clinical`)
- `governance_status` (`approved` vs `unverified` vs `synthetic`)
- `participant_count`, `session_count`, `image_count`, `usable_image_count`, `excluded_image_count`, `withdrawn_participant_count`
- `train_image_count`, `val_image_count`, `test_image_count`
- `creation_timestamp`
