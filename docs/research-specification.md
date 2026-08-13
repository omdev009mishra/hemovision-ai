# Research Specification

## 1. Intended Research Use

The HemoVision system is developed exclusively for scientific investigation to evaluate whether smartphone photographs of the human palpebral conjunctiva contain sufficiently reliable chromatic, spatial, and optical reflectance signals to estimate systemic hemoglobin (Hb) concentration and screen for anemia risk.

---

## 2. Primary Research Targets

The Machine Learning research roadmap focuses on three sequential modeling targets:

### Target A — Palpebral Conjunctiva Segmentation

* **Input**:
  ```text
  Eye photograph (Color RGB image containing the pulled-down lower eyelid region)
  ```
* **Output**:
  ```text
  Binary / Multi-class segmentation mask isolating the palpebral conjunctiva ROI
  ```
* **Evaluation Metrics**:
  * Dice Similarity Coefficient (DSC) $\ge 0.85$
  * Intersection over Union (IoU) $\ge 0.78$
  * Boundary Hausdorff Distance

---

### Target B — Anemia Risk Classification

* **Input**:
  ```text
  Segmented Conjunctiva ROI + Image Quality Metadata
  ```
* **Potential Output**:
  ```text
  • No evidence of anemia
  • Possible anemia
  • Unable to determine (Low quality / High uncertainty)
  ```
* **Evaluation Metrics**:
  * Area Under Receiver Operating Characteristic Curve (AUROC)
  * Sensitivity (Target: High sensitivity for screening recall)
  * Specificity
  * Out-of-Distribution / Low-Quality Rejection Rate

---

### Target C — Hemoglobin (Hb) Continuous Regression

* **Input**:
  ```text
  Segmented Conjunctiva ROI + Optical & Demographic Features
  ```
* **Potential Output**:
  ```text
  • Estimated Hb (g/dL)
  • 95% Prediction Interval (e.g., 11.2 ± 1.1 g/dL)
  • Model Confidence / Quality Index (0.0 to 1.0)
  ```
* **Evaluation Metrics**:
  * Mean Absolute Error (MAE in g/dL)
  * Root Mean Squared Error (RMSE)
  * Coefficient of Determination ($R^2$)
  * Bland-Altman Limits of Agreement against Laboratory Reference Hb

---

> [!WARNING]
> ### Crucial Non-Diagnostic Statement
> **Target B and Target C are research formulations for model optimization. The system DOES NOT currently achieve clinically validated diagnostic accuracy and MUST NOT be represented as providing accurate medical Hb measurements.**
