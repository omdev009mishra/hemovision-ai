# HemoVision — Secure Clinical Data Storage Architecture

## 1. Three-Zone Privacy Architecture

HemoVision strictly segregates data across three conceptual security zones:

```text
┌─────────────────────────────────────────────────────────────┐
│ ZONE A — IDENTIFIABLE SOURCE DATA (Enclave)                 │
│ Institution-controlled secure enclave.                      │
│ Contains real patient identity ↔ HV-P-XXXXXX mapping key.    │
│ NEVER committed to Git. NEVER exported outside institution. │
└──────────────────────────────┬──────────────────────────────┘
                               │ Pseudonymized Export
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ ZONE B — PSEUDONYMIZED RESEARCH DATA (Local / Cloud Storage) │
│ Contains pseudonymous IDs (HV-P-XXXXXX), sanitized images,   │
│ EXIF (no GPS/serials), sanitized lab reference values.      │
│ Stored in `dataset/clinical/` (Ignored by Git).             │
└──────────────────────────────┬──────────────────────────────┘
                               │ Code & Schemas Only
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ ZONE C — PUBLIC REPOSITORY (GitHub)                         │
│ Contains source code, JSON schemas, documentation, and      │
│ synthetic test fixtures ONLY. Zero real patient images/PII. │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. EXIF Privacy Safeguards

The `EXIFSanitizer` module strips all PII fields upon import:
- Stripped: `GPSInfo`, `GPSLatitude`, `GPSLongitude`, `DeviceSerialNumber`, `IMEI`, `MacAddress`.
- Retained for Research: Camera Make, Camera Model, Lens Type, Image Dimensions, Capture Timestamp.
