# HemoVision — Project Overview

## Architectural Vision & Motivation

Anemia affects approximately 1.62 billion people globally. It is characterized by a decrease in systemic hemoglobin (Hb) concentration or red blood cell count, leading to reduced oxygen-carrying capacity in blood.

Traditional screening requires invasive blood sampling (venipuncture or fingerstick), which creates logistical friction, infection risks, cost burdens, and reluctance in non-clinical or community screening environments.

**HemoVision** explores a non-invasive computer vision alternative: leveraging consumer smartphone cameras to capture images of the **palpebral conjunctiva** (the inner tissue lining of the lower eyelid) to estimate anemia risk and systemic hemoglobin concentration.

---

## Why Palpebral Conjunctiva?

1. **High Microvascularity**: The palpebral conjunctiva contains dense capillary networks situated close to the tissue surface.
2. **Minimal Melanin Interference**: Unlike external skin surfaces, the conjunctiva lacks significant epidermal melanin, reducing skin-tone reflectance confounding.
3. **Clinical Precedent**: Physical examination routinely involves inspecting conjunctival pallor as a qualitative sign of anemia. HemoVision aims to quantify and standardize this visual observation through objective computer vision metrics.

---

## High-Level System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    Mobile Device Capture                    │
│   • Guided Positioning (Distance, Focus, Lower Lid Pull)    │
│   • Ambient Light & Flash Calibration                       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Quality & Preprocessing Engine              │
│   • Eye Landmark Detection & ROI Bounding Box               │
│   • Quality Gates: Motion Blur, Occlusion, Specularity      │
│   • Color Normalization & Spectral Transform                │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  Segmentation & Modeling                    │
│   • Palpebral Conjunctiva Semantic Segmentation Mask        │
│   • Feature Extraction (RGB, HSV, LAB, Spatial Profiles)   │
│   • ML Model (Regression / Anemia Risk Classifier)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                Uncertainty & Decision Layer                 │
│   • Conformal Prediction Intervals & Reliability Score      │
│   • Output: Categorical Risk / Low Confidence Guidance      │
└─────────────────────────────────────────────────────────────┘
```

---

## Research Focus vs Diagnostic Claim

* **Research Focus**: Quantifying chromatic, morphological, and spectral reflectance properties of palpebral conjunctiva captured under uncontrolled smartphone lighting conditions, and establishing baseline statistical correlates with lab-certified Hb measurements.
* **Diagnostic Boundary**: HemoVision is strictly an investigational tool. It does **not** provide clinical diagnosis or actionable medical assessments during Phase 0–Phase 10 development.
