# Dataset Specifications & Schemas

This directory contains standard JSON Schemas defining data structures for clinical study participants, eye photographs, and ground-truth laboratory labels.

---

## Directory Structure

```text
dataset/
├── README.md                           # This document
├── schema/                             # Validated Draft-07 JSON Schemas
│   ├── participants.schema.json        # Participant demographic & clinical schema
│   ├── images.schema.json              # Image acquisition & hardware metadata schema
│   └── labels.schema.json              # Reference laboratory Hb & anemia label schema
├── metadata/                           # Local metadata JSON files (Gitignored)
└── samples/                            # Non-patient mock sample records (Gitignored)
```

---

## Data Privacy Reminder

> [!CAUTION]
> **No actual clinical dataset files or patient images may be committed to this folder or repository.**
> Local metadata JSON files placed in `metadata/` or image samples placed in `samples/` are automatically excluded from Git tracking via `.gitignore`.
