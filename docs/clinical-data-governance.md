# HemoVision — Clinical Data Governance Framework

## 1. Governance Classification States

Every dataset ingested or referenced by HemoVision is categorized into one of three strict governance states:

1. **`SYNTHETIC`**:
   - Safe for software unit testing, pipeline integration, and UI demonstrations only.
   - **`clinical_training_allowed: false`**.
2. **`UNVERIFIED_CLINICAL`**:
   - Clinical data exists locally or institutionally, but governance documentation (IRB/IEC approval reference, consent verification, data controller sign-off) is incomplete.
   - **`clinical_training_allowed: false`**. MUST NOT be used for ML training.
3. **`GOVERNED_CLINICAL`**:
   - Fully verified dataset with documented institutional ethics approval reference, verified participant consent, and data controller sign-off.
   - **`clinical_training_allowed: true`**. Only this state is eligible for clinical ML training.

---

## 2. Institutional Approval & Ethics Requirements

Institutional collection requires documented compliance before ingestion:
- **Ethics Approval Reference**: Must specify active IRB/IEC protocol number (e.g. `ETHICS_APPROVAL_REFERENCE_REQUIRED`).
- **Data Controller**: Designated institutional entity responsible for data protection.
- **Informed Consent**: Verified consent execution (`consent.schema.json`).
- **De-identification Verification**: Verified absence of PII (names, phone, email, Aadhaar, hospital MRNs, exact GPS).
