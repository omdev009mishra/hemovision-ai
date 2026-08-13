# Regulatory Notes & Quality Management Strategy

> [!NOTE]
> **DISCLAIMER**: This document is an internal software architecture and engineering planning guide. It does NOT constitute formal legal advice or regulatory submission filings.

---

## 1. Software as a Medical Device (SaMD) Framework

If HemoVision transitions from a research project toward commercial clinical deployment, it will qualify as **Software as a Medical Device (SaMD)**. 

### Target Risk Classification (Planning Assumptions)
* **US FDA**: Class II Medical Device (Special Controls; 510(k) Premarket Notification or De Novo Classification).
* **EU MDR (2017/745)**: Class IIa / IIb Rule 11 (Software intended to provide information used to take decisions for diagnostic or therapeutic purposes).
* **India CDSCO (Medical Devices Rules 2017)**: Class B / Class C Software Medical Device.

---

## 2. Applicable Medical Software Standards

Future engineering developments should align with key medical device software standards:

1. **IEC 62304 — Medical Device Software Lifecycle Processes**:
   * Requirement traceability (linking clinical user needs $\rightarrow$ software requirements $\rightarrow$ architecture $\rightarrow$ verification tests).
   * Configuration management and change control logging.
2. **ISO 14971 — Risk Management for Medical Devices**:
   * Hazard analysis (e.g., false negative anemia prediction leading to delayed treatment).
   * Risk mitigation controls (e.g., strict image quality gates rejecting unanalyzable photos).
3. **ISO 13485 — Quality Management Systems**:
   * Document control, software release tagging, and formal verification protocols.
4. **IEEE 2801 / Good Machine Learning Practice (GMLP)**:
   * Data integrity, model bias auditing, performance monitoring, and model drift tracking.

---

## 3. Data Privacy & Ethical Informed Consent

### Informed Consent Requirements
Clinical data collection protocols must receive prior approval from an Institutional Ethics Committee (IEC) or Institutional Review Board (IRB). Participant consent forms must explicitly specify:
* Intent to use anonymized ocular photographs for AI algorithm development.
* Participant right to withdraw data.
* Data encryption and storage protocols.

### Jurisdictional Privacy Compliance
* **United States**: HIPAA Privacy & Security Rules (De-identification standard 45 CFR § 164.514).
* **European Union**: General Data Protection Regulation (GDPR Article 9 — Special category health data).
* **India**: Digital Personal Data Protection Act (DPDP 2023) and DISHA guidelines.

---

## 4. Model Versioning & Traceability

To satisfy audit trail requirements:
- Every trained model binary must be immutably paired with its PyYAML configuration hash, training commit SHA, dataset version tag, and verification metric report.
- Model deployment packages must log on-device inference version numbers alongside output prediction intervals.
