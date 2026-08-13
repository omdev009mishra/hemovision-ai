# Dataset Specifications & Schemas

This directory contains standard JSON Schemas defining data structures for clinical study participants, eye photographs, and ground-truth laboratory labels, alongside synthetic dataset samples.

---

## Directory Structure

```text
dataset/
├── README.md                           # This document
├── schema/                             # Validated Draft 2020-12 JSON Schemas
│   ├── participants.schema.json        # Participant demographic & clinical schema
│   ├── images.schema.json              # Image acquisition & hardware metadata schema
│   └── labels.schema.json              # Reference laboratory Hb & anemia label schema
├── metadata/                           # Local metadata JSON files (Gitignored)
└── samples/                            # Synthetic fictional example records for testing
    ├── participant.example.json
    ├── image.example.json
    └── label.example.json
```

---

## ⚠️ Important Synthetic Data Warning

> [!WARNING]
> **Files under `dataset/samples/` are synthetic examples only and must never be replaced with real patient records.**

### Data Privacy & Storage Contracts
1. **Synthetic Examples Only**: All files under `samples/` contain strictly fictional data (`SYNTHETIC-P001`, `SYNTHETIC-IMG-001`) used to test schema validation pipelines.
2. **Zero Patient Data in Git**: No real patient health information (PHI), personally identifiable information (PII), or clinical eye images may ever be committed to Git.
3. **Secure Approved Storage**: Real research datasets must reside in secure, encrypted storage (e.g., HIPAA/GDPR-compliant cloud buckets or encrypted institutional servers).
4. **Pseudonymous Identifiers**: Participant IDs in clinical research data must use anonymized pseudonymous keys.
5. **Participant-Level Splitting**: All dataset splitting across train, validation, and test splits **MUST** be performed at the participant ID level to prevent data leakage.
6. **Continuous Integration**: JSON Schema validation is automatically enforced as part of the GitHub Actions CI pipeline (`.github/workflows/ci.yml`).
