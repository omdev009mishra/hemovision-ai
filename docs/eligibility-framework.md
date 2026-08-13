# Research Participant & Data Eligibility Framework

> [!IMPORTANT]
> **RESEARCH PROTOCOL TEMPLATE**: This document defines the formal research eligibility criteria for dataset curation. It represents an investigational framework requiring approval by an Institutional Ethics Committee (IEC) / Institutional Review Board (IRB) before real-world human data collection.

---

## 1. Inclusion Criteria

To be included in the curated HemoVision research dataset, a record must satisfy **ALL** of the following criteria:

1. **Informed Consent**: Participant (or legally authorized representative) has provided documented informed consent under an IEC/IRB-approved protocol.
2. **Valid Reference Laboratory Hb**: Participant has a verified reference laboratory hemoglobin measurement (`laboratory_hb_g_dl`) performed via an approved analytical reference method (`measurement_method`).
3. **Temporal Alignment**: Absolute time difference between reference blood draw and image capture (`time_delta_minutes`) is within the study protocol window (e.g. $\le 120$ minutes, or as defined by specific sensitivity protocol).
4. **Usable Ocular Image**: At least one conjunctival photograph passes automated and expert quality gates (`image_quality_status == "usable"`).
5. **Complete Baseline Metadata**: Required demographic and session metadata (`participant_id`, `age_years`, `sex`, `pregnancy_status`, `smoking_status`, `session_id`, `device_id`) are completely populated.

---

## 2. Exclusion Criteria

A participant or image record shall be **EXCLUDED** from dataset curation if **ANY** of the following criteria are met:

### Technical & Quality Exclusion Criteria
1. **Severe Motion or Out-of-Focus Blur**: Focus score (`focus_score`) falls below empirical sharpness threshold or image is flagged `rejected_blur`.
2. **Exposure Extremes**: Overexposed specular blowout (`overexposed_pixel_ratio > 0.15`) or underexposed darkness in palpebral mucosa (`rejected_exposure`).
3. **Conjunctiva Non-Visibility / Inadequate Eversion**: Lower eyelid is insufficiently pulled down, hiding the palpebral mucosa (`rejected_framing`).
4. **Severe Anatomical Occlusion**: Eyelashes, fingers, or specular glare obscure $> 25\%$ of the palpebral conjunctiva ROI (`rejected_occlusion`).

### Clinical & Protocol Exclusion Criteria
5. **Invalid / Unverified Laboratory Reference**: Laboratory blood sample marked as hemolyzed, clotted, or unverified (`lab_quality_status != "valid_verified"`).
6. **Out-of-Window Time Delta**: Time difference between image capture and blood draw exceeds study protocol limits.
7. **Ocular Pathology Interference**: Presence of active ocular surface infection, severe conjunctivitis, acute trauma, or pinguecula/pterygium covering the palpebral mucosa ROI.
8. **Withdrawal of Consent**: Participant revokes consent at any time (`consent_status == "withdrawn"`).
9. **Duplicate or Corrupted Record**: Duplicate participant identifier or unresolvable file corruption.
