# HemoVision — Conjunctiva Segmentation Benchmark Specification

## 1. Governance & Disclaimer

> [!CAUTION]
> **SYNTHETIC SOFTWARE VALIDATION ONLY**: All benchmark results in this repository are derived from synthetic image and mask fixtures. Synthetic segmentation results MUST NOT be interpreted as clinical accuracy, medical validity, or anemia diagnostic performance.

---

## 2. Evaluation Metrics Definitions

Let $P$ be the binary prediction mask and $G$ be the ground-truth binary mask.

- **Intersection over Union (IoU / Jaccard Index)**:
  $$\text{IoU} = \frac{|P \cap G|}{|P \cup G|}$$
- **Dice Similarity Coefficient (DSC)**:
  $$\text{Dice} = \frac{2 |P \cap G|}{|P| + |G|}$$
- **Precision**:
  $$\text{Precision} = \frac{|P \cap G|}{|P|}$$
- **Recall / Sensitivity**:
  $$\text{Recall} = \frac{|P \cap G|}{|G|}$$
- **Pixel Accuracy**:
  $$\text{Accuracy} = \frac{\text{True Positives} + \text{True Negatives}}{\text{Total Pixels}}$$

---

## 3. CLI Benchmark Commands

Execute single image segmentation:
```bash
python -m ml.src.segmentation.run_segmentation \
    --image dataset/samples/segmentation/synthetic_eye_001.png \
    --output research/results/segmentation/
```

Execute batch evaluation:
```bash
python -m ml.src.segmentation.benchmark \
    --dataset dataset/samples/segmentation \
    --output research/results/segmentation/
```
