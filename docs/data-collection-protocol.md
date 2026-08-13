# Data Collection Protocol & Leakage Protection

This document outlines the protocol for prospective data collection and the mandatory data leakage rules enforced across the HemoVision project.

---

## 1. Data Collection Fields

For each clinical study participant, the following structured dataset fields must be collected:

### Participant Demographics & Clinical Profile
* `participant_id`: Unique pseudonymous identifier (e.g., `HV-P-1002`).
* `age`: Age in completed years.
* `sex`: Biological sex assigned at birth (`male`, `female`, `intersex`).
* `pregnancy_status`: (`pregnant`, `not_pregnant`, `not_applicable`).
* `smoking_status`: (`non_smoker`, `active_smoker`, `former_smoker`).
* `skin_tone_fitzpatrick`: Fitzpatrick scale phototype (`I` through `VI`).
* `residence_altitude_m`: Altitude of primary residence in meters above sea level.

### Ground Truth Laboratory Reference
* `laboratory_hb_g_dl`: Quantitative hemoglobin level in g/dL.
* `cbc_rbc_count`: Red blood cell count ($10^6 / \mu\text{L}$) where available.
* `cbc_hematocrit_pct`: Hematocrit percentage where available.
* `lab_measurement_timestamp`: ISO 8601 timestamp of blood sample collection.
* `lab_measurement_method`: Equipment name / reference method (e.g., `Sysmex XN-1000`).

### Image & Capture Conditions
* `image_id`: Unique image UUID.
* `eye_side`: Left eye (`left`) or right eye (`right`).
* `phone_model`: Device hardware identifier (e.g., `Google Pixel 7`, `iPhone 14`).
* `camera_lens_type`: Main wide vs telephoto camera lens.
* `capture_timestamp`: ISO 8601 timestamp of photo capture.
* `lighting_condition`: (`indoor_ambient`, `indoor_led_flash`, `outdoor_shade`, `direct_sunlight`).
* `operator_id`: Anonymized clinician/research assistant ID.

---

## 2. 🛡️ MANDATORY DATA LEAKAGE PROTECTION

> [!CAUTION]
> ### PARTICIPANT-LEVEL DATA SPLITTING RULE
> **Data splitting across TRAIN, VALIDATION, and TEST sets MUST be executed strictly at the PARTICIPANT ID level.**

### ❌ FORBIDDEN (Image-Level Split)
Never place different photographs of the same participant into both train and test splits:
```text
Participant A (Image 1)  ──> TRAIN  ❌ INVALID DATA LEAKAGE
Participant A (Image 2)  ──> TEST   ❌ INVALID DATA LEAKAGE
```
*Why forbidden?* The model will memorize participant-specific background skin color, iris patterns, or facial geometry, yielding artificially inflated test accuracy that fails completely in real clinical deployment.

### ✅ MANDATORY (Participant-Level Split)
Partition participants holistically before extracting image samples:
```text
TRAIN SET
  ├── Participant A (Images 1, 2, 3)
  ├── Participant B (Images 1, 2)
  └── Participant C (Images 1, 2, 3, 4)

VALIDATION SET
  └── Participant D (Images 1, 2)

TEST SET (Strictly Held-Out)
  └── Participant E (Images 1, 2, 3)
```

---

## 3. Privacy & Storage Compliance

1. **Local Exclusion**: Raw dataset directories (`dataset/raw/`, `dataset/private/`) are ignored by `.gitignore`.
2. **No Patient PII**: Patient names, hospital ID numbers, and direct face images MUST NOT be stored in Git or public repositories.
