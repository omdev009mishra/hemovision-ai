# Clinical capture SOP — research template

**Use only under an approved, institution-controlled study protocol.** This SOP does not set a clinical threshold.

1. Confirm participant identity using the institution-controlled process.
2. Confirm the pseudonymous research ID.
3. Verify active consent.
4. Prepare the smartphone and clean the camera lens.
5. Standardize and record lighting.
6. Position the participant according to the approved protocol.
7. Capture the left eye.
8. Capture the right eye.
9. Capture the protocol-required burst for each eye.
10. Run the quality gate.
11. Repeat capture if quality fails, where permitted by the approved protocol.
12. Record camera and capture-environment metadata.
13. Complete the session and securely transfer the research data.

## Camera standardization record

Record, rather than assume, the actual front/rear camera policy and direction (preferred rear lens where protocol specifies), camera lens, image resolution, focus procedure, approximate distance guidance, orientation, lighting condition, ambient lux, flash policy, exposure policy, frames per eye, and left/right eye label. Phone serial numbers, IMEI, GPS, and other direct identifiers must not be retained.

## Quality gate

Assess focus, exposure, motion, framing, reflection, and conjunctiva visibility. Classify each image as `USABLE`, `REJECTED`, or `REVIEW_REQUIRED`. A rejected image must have one of: `BLUR`, `MOTION`, `OVEREXPOSURE`, `UNDEREXPOSURE`, `REFLECTION`, `OCCLUSION`, `BAD_FRAMING`, or `CONJUNCTIVA_NOT_VISIBLE`.

Run `ClassicalCVSegmenter` after quality review. If segmentation fails, mark `REVIEW_REQUIRED`; do not produce an Hb prediction.
