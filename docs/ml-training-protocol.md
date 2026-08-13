# HemoVision ML Training & Governance Protocol

## 1. Overview
This document specifies the research machine learning training protocol for HemoVision Hb estimation models using smartphone conjunctival images.

## 2. Governed Clinical Data Requirements
- Clinical model training requires an explicitly declared, governed clinical dataset with laboratory reference hemoglobin values (`laboratory_hb_g_dl`).
- Raw patient photographs and clinical identifiers are excluded from public Git tracking.
- Synthetic dataset samples under `dataset/samples/` are restricted to software verification and smoke tests.

## 3. Data Splitting & Leakage Prevention
- Partitioning **MUST** be performed at the `participant_id` level.
- Recommended ratios: TRAIN (70%), VALIDATION (15%), TEST (15%).
- Zero overlap is strictly enforced across splits:
  $$\text{Train} \cap \text{Val} = \emptyset, \quad \text{Train} \cap \text{Test} = \emptyset, \quad \text{Val} \cap \text{Test} = \emptyset$$

## 4. Cross-Validation
- `GroupKFold` grouped by `participant_id` is mandatory during cross-validation.
- Standard KFold is prohibited due to participant-level correlation.

## 5. Non-Fabrication Rule
- If no governed clinical dataset is available, model training output must report:
  `"Clinical training dataset unavailable — clinical model training not performed."`
- Synthetic smoke tests are labeled `SYNTHETIC SOFTWARE VALIDATION ONLY`.
