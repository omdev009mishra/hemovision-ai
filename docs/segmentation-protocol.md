# HemoVision — Palpebral Conjunctiva Segmentation Protocol

## 1. Overview & Research Scope

This document specifies the computer-vision architecture and anatomical protocol for localizing, segmenting, and extracting the **lower palpebral conjunctiva** (the vascularized inner mucous membrane of the lower eyelid) from smartphone ocular images.

> [!IMPORTANT]
> **Clinical Governance Notice**: Software validation and benchmarking are conducted exclusively using synthetic image fixtures. Performance demonstrated on synthetic fixtures does not establish clinical segmentation accuracy, medical validity, or diagnostic utility.

---

## 2. Target Anatomical Region

The target region is specifically the **lower palpebral conjunctiva**.

### Anatomical Exclusions:
- Bulbar sclera (white of the eye)
- Iris and cornea
- Upper palpebral conjunctiva
- Eyelashes and palpebral margin
- External palpebral skin and facial epidermis

---

## 3. Pipeline Architecture

```text
Input RGB Image
      ↓
Eye Region Detection (EyeDetector)
      ↓
Lower Eyelid Margin Localization (EyelidDetector)
      ↓
Multi-Colorspace Thresholding (HSV + CIELAB a*)
      ↓
Morphological Refinement & Filtering (MorphologicalRefiner)
      ↓
ROI Extraction & Quality Gate (ROIExtractor)
      ↓
Visual Overlay & Diagnostic Panel (SegmentationVisualizer)
```

---

## 4. Colorspaces & Engineering Parameters

All thresholds are managed via [`ml/configs/segmentation.yaml`](file:///d:/hemovision/ml/configs/segmentation.yaml):

- **CIELAB $a^*$ Channel**: Minimum $a^* = 135$ (emphasizes mucosal redness).
- **HSV Ranges**: Primary hue $[0, 25]$, Secondary hue $[160, 180]$, Saturation $[30, 255]$, Value $[40, 255]$.
- **Morphological Kernel**: Elliptical kernel $5 \times 5$.
- **Connected Components**: Minimum area $100 \text{ px}$, Aspect ratio $[0.5, 6.0]$.

---

## 5. Quality Gate & Failure Case Handling

If eye detection fails, morphological component area is $< 100 \text{ px}$, or coverage exceeds $> 45\%$, segmentation outputs:
- `success: false`
- `failure_reason: "eye_not_detected"` or `"segmentation_failed"`
- Upstream inference pipeline aborts downstream feature extraction and Hb estimation.
