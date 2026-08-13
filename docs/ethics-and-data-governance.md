# Ethics & Health Data Governance Policy

> [!IMPORTANT]
> **RESEARCH & GOVERNANCE POLICY**: This document defines the ethical principles, consent requirements, and governance controls for HemoVision research datasets. The repository and software are investigational tools and are NOT clinically certified.

---

## 1. Ethics Committee Approval & Informed Consent

1. **Institutional Review Board (IRB) / Institutional Ethics Committee (IEC)**: Prospective human subject data collection MUST NOT begin until formal written approval is granted by an accredited IRB/IEC.
2. **Informed Consent**: Every participant (or legal guardian) must sign an IRB/IEC-approved informed consent form detailing:
   * Voluntary participation.
   * Specific permission to capture ocular photographs for medical AI research.
   * Pseudonymous data processing rights.
   * Right to withdraw from the study at any time without impacting medical care.

---

## 2. Participant Pseudonymization & Identity Scrubbing

* **Zero Direct PII/PHI**: Participant names, birth dates, hospital record numbers, addresses, phone numbers, and direct facial photographs MUST NEVER be collected in project metadata or stored in software repositories.
* **Pseudonymous Keys**: All clinical records are bound exclusively to study-generated pseudonymous keys (`participant_id`, `session_id`, `operator_id`, `device_id`).
* **Offline Master Key Storage**: The master key linking `participant_id` to actual hospital medical record identity is maintained offline in a secure, encrypted hospital database accessible only to authorized principal investigators.

---

## 3. Data Governance & Security Access Control

1. **Least Privilege Access**: Access to encrypted raw research datasets (images, lab results, metadata) is restricted strictly to credentialed research team members bound by non-disclosure agreements (NDAs).
2. **No Clinical Data in Git**: Raw clinical images, DICOM/PNG files, and patient spreadsheets MUST NEVER be committed to Git. Ignored via `.gitignore`.
3. **Controlled Dataset Exports**: Derived research dataset exports (e.g. `v0.1.0`) must be approved by the Data Governance Board prior to distribution to collaborating academic institutions.
4. **Participant Consent Withdrawal Handling**: If a participant revokes consent, their `consent_status` is updated to `"withdrawn"`, and all associated image, session, and reference records are immediately purged from active training, validation, and test datasets.
5. **Data Retention & Deletion**: Datasets are retained for the duration specified in the IRB/IEC protocol and securely wiped using DoD 5220.22-M sanitation standards upon study termination.
