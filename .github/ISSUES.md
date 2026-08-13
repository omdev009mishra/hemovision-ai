# HemoVision — Initial GitHub Issue Board

This document lists the 10 core GitHub issues created to track Phase 0 through Phase 7 milestones.

---

### Issue 1
* **Title**: `Phase 0: Establish repository foundation`
* **Labels**: `phase-0`, `infrastructure`, `documentation`
* **Description**: Create complete directory tree, medical disclaimer README, security rules, dataset JSON schemas, research specs, and CI testing workflow.
* **Status**: Completed in Phase 0.

---

### Issue 2
* **Title**: `Phase 1: Define clinical dataset specification`
* **Labels**: `phase-1`, `clinical`, `specification`
* **Description**: Define anonymized participant demographic schemas, clinical laboratory reference protocols, and participant-isolated data split rules.

---

### Issue 3
* **Title**: `Phase 1: Define image acquisition protocol`
* **Labels**: `phase-1`, `camera`, `protocol`
* **Description**: Establish standardized smartphone camera capture conditions, illumination guidelines (ambient vs LED flash), focal distance, and lower eyelid retraction techniques.

---

### Issue 4
* **Title**: `Phase 1: Define annotation protocol`
* **Labels**: `phase-1`, `annotation`, `segmentation`
* **Description**: Finalize COCO-compliant JSON format for palpebral conjunctiva polygon boundaries, quality flag tags, and annotator agreement metrics.

---

### Issue 5
* **Title**: `Phase 2: Build smartphone eye capture prototype`
* **Labels**: `phase-2`, `mobile`, `camera-prototype`
* **Description**: Develop native camera capture interface with spatial reticle overlays for palpebral conjunctiva positioning and flash calibration.

---

### Issue 6
* **Title**: `Phase 3: Implement conjunctiva segmentation baseline`
* **Labels**: `phase-3`, `ml`, `segmentation`
* **Description**: Implement U-Net / MobileNetV3 semantic segmentation model to auto-crop palpebral conjunctiva mucosa with DSC $\ge 0.85$.

---

### Issue 7
* **Title**: `Phase 4: Implement image quality assessment`
* **Labels**: `phase-4`, `ml`, `quality-control`
* **Description**: Build automated blur, overexposure, and lid occlusion detection module to reject unanalyzable images prior to ML inference.

---

### Issue 8
* **Title**: `Phase 5: Train first Hb prediction baseline`
* **Labels**: `phase-5`, `ml`, `regression`
* **Description**: Train initial baseline regression model (e.g., ResNet/EfficientNet + color features) estimating Hb (g/dL) with uncertainty bounds.

---

### Issue 9
* **Title**: `Phase 6: Build model evaluation pipeline`
* **Labels**: `phase-6`, `ml`, `evaluation`, `bias-audit`
* **Description**: Create participant-isolated evaluation runner measuring MAE, RMSE, Bland-Altman agreement, and bias across Fitzpatrick skin tones and phone models.

---

### Issue 10
* **Title**: `Phase 7: Build Flutter mobile application`
* **Labels**: `phase-7`, `mobile`, `flutter`
* **Description**: Develop cross-platform Flutter application integrating guided capture UI, real-time quality feedback, and local inference execution.
