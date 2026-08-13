# Contributing to HemoVision

Thank you for contributing to **HemoVision**. This project is dedicated to rigorous, open, and reproducible research into non-invasive anemia screening using computer vision and medical AI.

---

## Engineering & Research Principles

All contributions to HemoVision must adhere strictly to the following 7 core engineering principles:

### 1. Reproducibility
Every experiment, model build, and metric report must be 100% reproducible.
- Always log configuration parameters (PyYAML configs in `ml/configs/`).
- Record explicit random seeds across NumPy, PyTorch, and Python random modules.
- Maintain dataset versioning and track Git commit hashes alongside model artifact metrics.

### 2. Patient-Level Isolation (Zero Data Leakage)
**Never split datasets at the image level.**
- All data splitting (train / validation / test) **MUST** be performed strictly at the **participant ID level**.
- If Participant A has 5 conjunctival photographs, all 5 photographs must reside within the *same* split (e.g., all in TRAIN). Placing images of Participant A into both TRAIN and TEST invalidates model evaluation due to spatial/spectral data leakage.

### 3. Explainability & Interpretability
Black-box medical predictions are unacceptable.
- Model architectures should support saliency visualization (e.g., Grad-CAM, Integrated Gradients, attention maps).
- Feature extraction modules must retain human-interpretable color space signals (e.g., CIELAB, HSV, spectral reflectance proxies) alongside deep spatial embeddings.

### 4. Explicit Uncertainty & Reliability Assessment
Medical decision support systems must know when they do not know.
- Models must provide confidence estimates, prediction intervals, or out-of-distribution indicators.
- Pipeline outputs must include a discrete state for low-confidence or unanalyzable inputs (`Unable to determine`).

### 5. Safety & Truthfulness
- Never fabricate or overstate diagnostic certainty.
- Never use synthetic or unverified internet images as clinical ground truth.
- Always surface clear disclaimers in user interfaces and technical metrics reports.

### 6. Health Data Privacy & Anonymization
- **NEVER** commit patient identifiable information (PII / PHI), raw clinical photographs, or real lab records to Git.
- Use pseudonymous Participant IDs (e.g., `HV-PART-001042`).
- All raw datasets must be stored in secure, encrypted local/cloud storage listed in `.gitignore`.

### 7. Modularity & Clean Architecture
Keep system components decoupled and cleanly isolated under `ml/src/`:
- `data/`: Dataset parsing, validation, and loading.
- `preprocessing/`: Color space transformations, illumination normalization, resizing.
- `segmentation/`: Palpebral conjunctiva ROI detection and masking.
- `quality/`: Motion blur, exposure, and occlusion assessment.
- `models/`: Neural network and ML model architecture definitions.
- `training/`: Training loops, loss functions, optimizer setups.
- `evaluation/`: Metrics computation (MAE, RMSE, R², Sensitivity, Specificity, Confusion matrices).
- `inference/`: On-device and server inference pipeline wrappers.

---

## Development & Branching Workflow

We follow a structured phase-based branching workflow:

```text
main
 └── phase-0-foundation
 └── phase-1-dataset
 └── phase-2-camera
 └── phase-3-segmentation
 ...
```

### Pull Request Lifecycle
1. **Branch**: Create a feature branch off `main` or the active phase branch (e.g., `feature/seg-unet-baseline`).
2. **Implementation**: Write clean, modular code following standard PEP 8 formatting.
3. **Tests**: Add unit tests under `ml/tests/` verifying functional behavior.
4. **Documentation**: Update corresponding markdown files in `docs/` or module READMEs.
5. **Validation**: Run `pytest` locally to confirm all tests pass.
6. **Pull Request**: Open a PR with a clear summary of changes, rationale, and metric impacts.
7. **Merge**: PR must be reviewed and pass automated CI checks before merging.

---

## Code Quality Standards

- Python code must pass standard syntax and style checks.
- Add type hints (`typing`) to public function signatures.
- Write docstrings (`Google style`) for all modules, classes, and non-trivial functions.
