# Informed-consent workflow

Participant
→ Study explanation
→ Questions answered
→ Consent document presented
→ Voluntary consent
→ Consent verified
→ Pseudonymous participant ID generated
→ Data collection allowed

Consent is obtained and maintained using the institution-controlled process and the approved consent version. The research dataset contains only minimum consent metadata: consent ID, pseudonymous participant ID, consent version/timestamp/status, withdrawal status/timestamp, and pseudonymous operator ID.

- If consent is absent, pending, or withdrawn: **NO IMAGE COLLECTION**.
- If consent is withdrawn: exclude the participant from future ML datasets according to the approved protocol and applicable requirements.
- Never store signed consent documents in Git, research reports, audit logs, or the application repository.
