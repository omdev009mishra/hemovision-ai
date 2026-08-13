# Machine Learning Framework & Pipeline

This directory contains the modular Python packages, experiment configurations, training code, and test suites for the HemoVision machine learning pipeline.

---

## Directory Architecture

```text
ml/
├── README.md                   # This document
├── requirements.txt            # Pinned Python dependency environment
├── configs/                    # Yaml configurations for experiments
│   └── .gitkeep
├── notebooks/                  # Exploratory research notebooks
│   └── .gitkeep
├── src/                        # Main modular Python source package
│   ├── data/                   # Dataset parsing, validation, and loaders
│   ├── preprocessing/          # Color normalization & ISP transformation
│   ├── segmentation/           # Palpebral conjunctiva ROI segmentation models
│   ├── quality/                # Quality assessment & blur/exposure gates
│   ├── models/                 # Neural network architectures
│   ├── training/               # Training loops, losses, & optimizers
│   ├── evaluation/             # Metrics, validation loss, & performance reports
│   └── inference/              # Local runtime inference pipeline wrappers
└── tests/                      # Pytest unit testing suite
    └── test_schemas.py
```

---

## 🎯 Primary First ML Objective: Palpebral Conjunctiva Segmentation

The initial machine learning objective of HemoVision is **Target A — Palpebral Conjunctiva Segmentation**.

Before attempting any hemoglobin modeling or anemia risk estimation:
1. Accurate, automated semantic segmentation of the palpebral conjunctiva mucosa must be established.
2. Quality gating (detecting out-of-focus blur, overexposure, and lid occlusion) must be implemented.

**Hb estimation models (Target B / Target C) will NOT be implemented during Phase 0 or Phase 3 segmentation baselines until ROI extraction and quality gating achieve validated benchmarks.**
