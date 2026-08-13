# Security & Health Data Privacy Policy

Security, data privacy, and ethical compliance are fundamental to the **HemoVision** research project.

---

## 🔒 Mandatory Data Protection Rules

To protect patient privacy, prevent unauthorized access to sensitive Protected Health Information (PHI) or Personally Identifiable Information (PII), and adhere to global healthcare standards (HIPAA, GDPR, DPDP Act India), all contributors **MUST STRICTLY OBEY** the following rules:

### 1. Zero Clinical Data in Version Control
- **NEVER** commit real patient images or eye photographs to Git repositories.
- **NEVER** commit patient names, birthdates, national identifiers, phone numbers, or addresses.
- **NEVER** commit raw clinical laboratory reports, hospital record scans, or medical spreadsheets.
- **NEVER** commit `.env` files, API keys, credentials, tokens, or private RSA/SSH keys.

### 2. Pseudonymous Identifiers Only
- All participant records used in research workflows must use anonymized, synthetic, or pseudonymous participant IDs (e.g., `HV-P-90812`).
- Mapping tables linking pseudonymous IDs to actual clinical trial participant identity must be kept entirely offline in secure, encrypted hospital databases inaccessible to the public repository.

### 3. External Dataset Storage
- Research datasets (images, masks, ground truth lab tables) must reside outside the Git workspace directory or within gitignored local paths (such as `dataset/raw/`, `dataset/private/`, `data/raw/`).
- Shared research datasets among approved investigators must be transferred via secure, encrypted cloud storage (e.g., AWS S3 with KMS encryption, HIPAA-compliant cloud drives) with access control logging.

### 4. Git Pre-Commit & Credential Prevention
Before pushing code to remote repositories, verify that no sensitive files or environment variables are tracked:
```bash
git status
git check-ignore -v dataset/private/*
```

---

## 🚨 Reporting a Vulnerability or Data Exposure Incident

If you discover a security vulnerability, an accidental exposure of credentials, or any data privacy issue within this repository:

1. **DO NOT** create a public GitHub Issue describing the vulnerability or exposure.
2. Email the core research lead directly at: **security@hemovision-research.org** (or contact the repository maintainers privately).
3. Include details of the affected file, commit hash, or component.
4. The maintainers will acknowledge receipt within 24 hours and take immediate steps to remediate, revoke credentials, or scrub Git history using `git-filter-repo` if necessary.
