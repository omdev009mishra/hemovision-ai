# Phase 1 — Dataset & Clinical Collection Specification

**Status:** Design specification — no participant recruitment or clinical data collection is authorized by this document alone.

## 1. Purpose

Phase 1 defines the data contract and collection protocol required to investigate smartphone-based palpebral conjunctiva imaging for anemia screening and hemoglobin (Hb) estimation.

The primary objective is to create a reproducible dataset in which each eye image can be linked, through pseudonymous identifiers, to an appropriately timed laboratory Hb reference measurement and the contextual variables needed to evaluate confounding, generalization, and safety.

## 2. Research Scope

The dataset supports three research targets:

1. **Conjunctiva segmentation** — identify the palpebral conjunctiva in an eye image.
2. **Anemia-risk classification** — evaluate whether image-derived information can discriminate study-defined anemia categories.
3. **Hb regression** — investigate prediction of laboratory Hb as a continuous target.

The dataset must not be interpreted as establishing diagnostic accuracy. Any future clinical claim requires an appropriately designed validation study.

## 3. Unit of Observation

The fundamental research unit is the **participant**. Images are repeated observations nested within participants.

A participant may contribute:

- one or both eyes;
- multiple captures under the defined protocol;
- repeated visits only when explicitly allowed by the study protocol.

The participant ID must remain stable across all associated records.

## 4. Required Record Linkage

The minimum linkage is:

```text
Participant
    │
    ├── Image 1 ──┐
    ├── Image 2 ──┼── Laboratory reference record
    └── Image 3 ──┘
```

Every linkage must use pseudonymous IDs. Names, hospital registration numbers, phone numbers, addresses, or other direct identifiers must remain outside the research dataset and Git repository.

## 5. Ground Truth

The primary continuous reference target is laboratory-measured Hb in g/dL.

For each reference measurement record, capture:

- measurement timestamp;
- measurement method;
- instrument/manufacturer when available;
- specimen type where relevant;
- study/site identifier;
- whether the result is valid for analysis.

Categorical anemia labels must be derived from the **pre-specified study analysis protocol** using an authoritative clinical reference. Do not encode a universal cutoff directly into the dataset schema.

WHO's 2024 guideline emphasizes that Hb-based anemia assessment requires consideration of population characteristics and context; therefore categorical labels must remain versioned and protocol-specific. citeturn0search2

## 6. Timing

Record the exact image-capture timestamp and laboratory measurement timestamp so that the time delta can be calculated during analysis.

Do not assume a universal acceptable time window in the data schema. The study protocol must define the allowable window for each analysis, document exceptions, and perform sensitivity analyses when appropriate.

## 7. Participant-Level Covariates

Collect only variables justified by the study protocol and ethics approval. Candidate variables include:

- age;
- sex;
- pregnancy status where applicable;
- smoking status;
- relevant altitude exposure;
- relevant systemic conditions;
- relevant ocular conditions;
- medications or acute interventions that could affect Hb or ocular appearance, where scientifically justified.

Skin phototype or other appearance-related variables may be collected only when there is a documented scientific purpose, a validated collection procedure, and appropriate ethics/privacy approval. Do not treat such variables as proxies for race or ethnicity.

## 8. Image-Level Metadata

For every captured image record, collect:

- image ID;
- participant ID;
- eye side;
- capture timestamp;
- smartphone manufacturer/model;
- camera/lens information where available;
- image dimensions;
- lighting protocol;
- exposure metadata where available;
- focus/quality metrics;
- operator/research-session pseudonymous ID;
- annotation status;
- rejection reason when unusable.

## 9. Image Acquisition Standardization

The future collection application should guide the operator through a controlled capture workflow:

1. Confirm participant/session ID.
2. Confirm consent/eligibility status.
3. Position the participant consistently.
4. Capture the lower eyelid/conjunctiva using the prescribed camera configuration.
5. Capture multiple frames where the protocol requires it.
6. Record lighting and device metadata automatically where possible.
7. Run an image-quality gate before accepting a frame.
8. Store only the pseudonymous image ID in the research metadata layer.

The exact camera distance, illumination, exposure behavior, and eyelid positioning must be frozen in a versioned acquisition protocol before formal data collection.

## 10. Image Quality Gate

Each image should be assigned quality indicators for at least:

- focus/blur;
- exposure;
- motion;
- occlusion;
- conjunctival visibility;
- framing;
- specular reflection;
- capture-angle deviation.

An unusable image should be retained as a **quality-control record** when policy permits, but must not be silently included in model training.

## 11. Dataset Splitting

Splitting must occur at the participant level.

```text
TRAIN       → unique participants only
VALIDATION  → different participants only
TEST        → completely held-out participants
```

No participant may appear in more than one split.

If multiple collection sites, phones, or time periods are available, preserve an additional external/generalization test set where feasible. This follows good ML practice emphasizing representative clinical datasets and independence between training and test data. citeturn0search0turn0search24

## 12. Versioning

Every dataset release must have a version identifier, for example:

```text
HV-DATA-0.1.0
```

Record:

- schema version;
- acquisition protocol version;
- annotation protocol version;
- inclusion/exclusion version;
- label-definition version;
- preprocessing version;
- creation date;
- responsible study team.

## 13. Data Exclusion

Potential exclusion categories include:

- invalid consent/authorization status;
- duplicate participant/session records;
- invalid laboratory reference;
- image not containing the target anatomy;
- severe blur or exposure failure;
- protocol violation;
- corrupted image;
- unresolved linkage between image and reference measurement.

Every exclusion should have a machine-readable reason code rather than silent deletion.

## 14. Ethics and Privacy Gate

No prospective participant collection should begin until the responsible research team has established the applicable ethics/IRB process, consent materials, data-management plan, and site permissions.

This repository must never contain identifiable participant data or raw clinical images.

## 15. Phase 1 Deliverables

Phase 1 is complete when the repository contains:

- a frozen dataset schema;
- a versioned collection protocol;
- a participant eligibility framework;
- a consent/data-governance framework;
- a controlled image-acquisition protocol;
- a laboratory-reference protocol;
- an annotation/data-quality plan;
- a participant-level splitting policy;
- a dataset versioning policy;
- a data dictionary;
- a pilot-readiness checklist.

No ML model training is required to close Phase 1.
