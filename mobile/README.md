# HemoVision — Smartphone Conjunctival Imaging Prototype (`hemovision_capture`)

> **RESEARCH PROTOTYPE ONLY**  
> **DISCLAIMER:** This application is strictly an experimental data-acquisition prototype for computer vision research. It does **NOT** diagnose anemia, predict hemoglobin (Hb) concentrations, estimate physiological parameters, or provide medical advice/clinical decision support.

---

## Overview

`hemovision_capture` is a Flutter-based mobile application built to standardise smartphone image acquisition of the palpebral conjunctiva (inner lower eyelid). 

The sole objective of Phase 2 is:
> "Reliably capture high-quality smartphone images of the lower palpebral conjunctiva and generate research-compatible metadata."

---

## Architecture & Features

- **Feature-First Clean Architecture:** Organised into `core/`, `models/`, `services/`, `widgets/`, `screens/`, and `app/`.
- **On-Device Quality Engine (`QualityEngine`):**
  - **Focus Estimation:** Laplacian variance convolution score ($>100.0$ threshold heuristic).
  - **Exposure Analysis:** Pixel intensity histogram (overexposed $>240$, underexposed $<15$).
  - **Frame Selection:** Automatically selects the best frame from burst captures ($3\text{--}5$ frames).
  - **Disclaimer:** Quality thresholds are unvalidated engineering heuristics, not clinical metrics.
- **Sensor Integration (`SensorService`):** Accelerometer stability monitoring during image capture.
- **Schema-Aligned Metadata (`MetadataService` & `StorageService`):**
  - Serialises `session_metadata.json` and `frame_XXX_metadata.json` matching Phase 1 JSON Schemas.
  - Generates synthetic participant IDs (`HV-TEST-P-XXXXXXXX`) and UUID v4 IDs.
  - Stores all data in application-private local storage (`path_provider`).

---

## Privacy & Security

1. **Zero PHI / PII:** No free-text participant name, phone, email, or medical history entry fields.
2. **Local Application-Private Storage:** Data is stored exclusively in local app-private storage (`path_provider`).
3. **No Cloud Sync:** No Firebase, S3, or remote API endpoints. Zero network transmission.

---

## Build & Run

### Prerequisites
- Flutter SDK 3.48+ / Dart 3.12+
- Android SDK 24+ (Android 7.0 Nougat minimum)

### Setup & Testing
```bash
cd mobile/hemovision_capture

# Run static analysis
flutter analyze

# Run unit and widget tests
flutter test

# Build debug APK
flutter build apk --debug
```
