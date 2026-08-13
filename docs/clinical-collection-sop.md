# HemoVision — Clinical Data Collection Standard Operating Procedure (SOP)

## 1. Prerequisites
1. Verified institutional IRB/IEC approval.
2. Verified active informed consent signed by participant.
3. Pseudonymous research participant ID generated in Zone A (`HV-P-XXXXXX`).

---

## 2. Step-by-Step Acquisition Procedure

1. **Informed Consent**: Obtain consent and record `HV-CNS-XXXXXX` in `consent.schema.json`.
2. **Participant Variables**: Record age, biological sex, pregnancy status, smoking, altitude, skin phototype.
3. **Environment Setup**: Position participant under standardized lighting (diffuse ambient or controlled research LED). Record ambient lux.
4. **Conjunctival Exposure**: Operator gently everts lower eyelid exposing palpebral mucosa.
5. **Mobile Capture**:
   - Select Front or Rear Camera in HemoVision mobile capture app.
   - Align eye within target reticle.
   - Capture left eye burst (3 images) and right eye burst (3 images).
6. **Quality Gate Verification**: Confirm instant quality pass (blur, exposure, framing, conjunctiva visibility).
7. **Laboratory Ground Truth Reference**: Collect venous blood sample within protocol window ($\le 120 \text{ minutes}$). Record laboratory Hb ($g/dL$) from automated hematology analyzer.
8. **Sanitization & Ingestion**: Run `python -m ml.src.data.import_dataset --input <raw_dir> --output dataset/clinical`.
