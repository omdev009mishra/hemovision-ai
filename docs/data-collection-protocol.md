# Data Collection Protocol & Standard Operating Procedure

This document defines the 14-step standard operating procedure (SOP) for data collection and dataset ingestion in HemoVision.

> [!CAUTION]
> ### 🛡️ STRICT HEALTH DATA PRIVACY MANDATE
> **RAW CLINICAL DATA, PATIENT PHOTOGRAPHS, AND IDENTIFIABLE HEALTH RECORDS MUST NEVER BE STORED IN GIT OR PUBLIC REPOSITORIES.**
> All real clinical datasets must be kept in encrypted, HIPAA/GDPR-compliant cloud buckets or secure local servers listed in `.gitignore`.

---

## 14-Step Clinical Data Collection & Ingestion Workflow

```text
STEP 1: Participant Registration
   │
STEP 2: Consent Verification
   │
STEP 3: Participant Metadata Recording
   │
STEP 4: Laboratory Hb Reference Blood Draw
   │
STEP 5: Capture Session Initialization
   │
STEP 6: Phone / Device Metadata Logging
   │
STEP 7: Lighting & Environment Metadata Logging
   │
STEP 8: Left-Eye Image Capture (Burst Mode)
   │
STEP 9: Right-Eye Image Capture (Burst Mode)
   │
STEP 10: Immediate On-Device Image Quality Gate
   │
STEP 11: Laboratory-Reference Linkage
   │
STEP 12: Independent Data Quality & Referential Integrity Review
   │
STEP 13: Encrypted Secure Storage & PII Scrubbing
   │
STEP 14: Dataset Versioning & Participant-Isolated Splitting
```

---

### Step Detail Specifications

#### STEP 1 — Participant Registration
Assign a unique pseudonymous `participant_id` (e.g. `HV-P-1002`). Master key linking real patient identity to `participant_id` remains offline in encrypted hospital database.

#### STEP 2 — Consent Verification
Verify documented informed consent under an IEC/IRB-approved protocol (`consent_status = "verified_active"`).

#### STEP 3 — Participant Metadata
Record `age_years`, `sex`, `pregnancy_status`, `smoking_status`, `skin_phototype`, `residence_altitude_m`, and comorbidities according to the [Data Dictionary](file:///d:/hemovision/docs/data-dictionary.md).

#### STEP 4 — Laboratory Hb Reference Measurement
Perform venous blood draw or microcuvette capillary sampling. Record `laboratory_hb_g_dl`, `measurement_timestamp`, `measurement_method`, and instrument specifications.

#### STEP 5 — Capture Session Initialization
Generate a unique `session_id` linking operator, device, location, and timestamp.

#### STEP 6 — Phone / Device Metadata
Log `phone_manufacturer`, `phone_model`, `camera_lens_type`, and pseudonymous `device_id`. Never record IMEI or hardware serials.

#### STEP 7 — Lighting / Environment Metadata
Log `capture_environment`, `lighting_condition`, `ambient_lux` (if illuminance sensor available), and `color_temperature_kelvin`.

#### STEP 8 — Left-Eye Capture
Pull down left lower eyelid to evert palpebral mucosa. Capture a 3–5 frame burst image sequence under controlled framing.

#### STEP 9 — Right-Eye Capture
Pull down right lower eyelid to evert palpebral mucosa. Capture a 3–5 frame burst image sequence under controlled framing.

#### STEP 10 — Image Quality Check
Run automated sharpness (`focus_score`) and exposure (`exposure_info`) gates. Reject unusable frames (`rejected_blur`, `rejected_exposure`).

#### STEP 11 — Laboratory-Reference Linkage
Link `lab_measurement_id` to `participant_id` and compute `time_delta_minutes` between image capture and blood draw.

#### STEP 12 — Data Quality Review
Execute deterministic metadata validation using `ml/src/data/validate_dataset.py` to confirm referential integrity and zero duplicate IDs.

#### STEP 13 — Secure Storage
Transfer anonymized image files and JSON metadata to encrypted HIPAA/GDPR-compliant cloud/server storage.

#### STEP 14 — Dataset Versioning & Splitting
Assign dataset release version tag (e.g. `v0.1.0`) and partition participants into TRAIN, VALIDATION, and TEST sets enforcing strict participant-level isolation.
