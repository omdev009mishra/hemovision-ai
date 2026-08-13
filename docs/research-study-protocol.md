# RESEARCH PROTOCOL TEMPLATE

**Status:** This document is a template until formally approved by the responsible institution. It does not indicate ethics, IRB, IEC, CDSCO, regulatory, clinical-validation, or medical-device approval.

## 1. Study title

HemoVision: controlled research preparation for smartphone lower-palpebral-conjunctiva image collection and laboratory hemoglobin linkage.

## 2. Research objective

Evaluate whether smartphone images of the lower palpebral conjunctiva contain measurable visual information associated with laboratory-measured hemoglobin concentration.

## 3. Primary research question

Under the approved acquisition and laboratory-reference protocol, is there an investigable association between the collected image information and laboratory-measured hemoglobin concentration?

## 4. Secondary research questions

Assess acquisition feasibility, image-quality outcomes, segmentation success, metadata completeness, image-to-laboratory linkage, and operator workflow reliability. No diagnostic or accuracy claim is an endpoint of this template.

## 5. Study population

The approved protocol must define the study setting, recruitment pathway, population, sample size rationale, and any age restrictions.

## 6. Inclusion criteria

Only institutionally approved, protocol-versioned criteria may be used. Candidate criteria are documented in [participant eligibility](participant-eligibility.md).

## 7. Exclusion criteria

Only institutionally approved, protocol-versioned criteria may be used. No medical exclusion criterion in this repository is clinically validated.

## 8. Participant workflow

Institution-controlled identity confirmation; study explanation; questions; voluntary consent; consent verification; pseudonymous ID; approved capture; laboratory-reference linkage; secure transfer. No image collection occurs without verified consent.

## 9. Image acquisition workflow

Follow the [clinical capture SOP](clinical-capture-sop.md): standardized camera, lighting, orientation, left/right labels, burst frames, quality gate, ClassicalCV segmentation, and ROI review. The collection workflow never produces an Hb prediction.

## 10. Laboratory Hb reference workflow

Laboratory results originate only from the approved laboratory process described in the [laboratory-reference SOP](laboratory-reference-collection-sop.md). Image-derived estimates are never ground truth.

## 11. Timing/alignment requirements

The approved protocol must set an alignment window. `LabAligner` records image timestamp, laboratory timestamp, selected measurement, time delta, and alignment status; it does not invent a clinical cutoff.

## 12. Data-quality criteria

Each image is classified `USABLE`, `REJECTED`, or `REVIEW_REQUIRED` for focus, exposure, motion, framing, reflection, and conjunctiva visibility. Segmentation failure requires review. Rejected images carry a rejection reason.

## 13. Dataset splitting

Any later research analysis must use participant-level isolated splits. A participant cannot appear in more than one split. Dataset freeze verifies this condition.

## 14. Statistical analysis plan

The formally approved statistical analysis plan must pre-specify estimands, sample-size rationale, analysis population, uncertainty reporting, and handling of protocol deviations. This template makes no diagnostic-performance commitment.

## 15. Missing-data handling

Use explicit states: `MISSING`, `NOT_COLLECTED`, `NOT_APPLICABLE`, `WITHDRAWN`, and `INVALID`. Do not replace missing values with zero or impute laboratory Hb during collection.

## 16. Withdrawal handling

Record withdrawal status and timestamp. Exclude withdrawn participants from future ML datasets according to the approved protocol and applicable requirements; retain only permissible audit metadata.

## 17. Privacy/data governance

Store only pseudonymous research metadata. Direct identifiers, signed consent documents, laboratory reports, hospital identifiers, device serial numbers, GPS data, credentials, and participant images are not committed to Git. Retention and access follow the approved institutional plan.

## 18. Safety considerations

This is investigational research preparation, not a diagnostic service. Do not use any output for medical decisions, diagnosis, treatment, or replacement of laboratory testing.

## 19. Limitations

Smartphone optics, illumination, positioning, image quality, segmentation, population coverage, and laboratory timing can affect data suitability. No clinical dataset or clinical model is available in this repository.

## 20. Study completion criteria

The approved protocol must define completion and dataset-freeze criteria. At minimum, governance, consent, schema, PII/EXIF privacy, quality, segmentation, lab alignment, withdrawals, and participant-level split checks must be reviewed before freezing.
