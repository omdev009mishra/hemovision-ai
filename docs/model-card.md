# HemoVision Model Card: Hb Estimator (v0.1.0 Research)

## Model Overview
- **Model Name**: HemoVision Hb Estimator
- **Model Version**: `hb-v0.1.0`
- **Architecture**: Ridge Regression / Baseline Ensemble on 28 quantitative features
- **Scope**: Experimental non-diagnostic research prototype

## Feature Input Vector (28 Features)
1. `mean_R`, `mean_G`, `mean_B`, `std_R`, `std_G`, `std_B`
2. `mean_RG_ratio`, `mean_RB_ratio`, `mean_GB_ratio`
3. `mean_L`, `mean_a`, `mean_b`, `std_L`, `std_a`, `std_b`
4. `median_a`, `median_b`, `p10_a`, `p90_a`, `p10_b`, `p90_b`
5. `mean_hue`, `mean_saturation`, `mean_value`
6. `texture_mean`, `texture_std`, `ROI_area_ratio`, `specularity_ratio`

## Limitations & Intended Use
- **Not for Clinical Diagnosis**: Estimates are research approximations and must not replace laboratory blood testing.
- **Quality Gating**: Rejected images (blur/exposure) bypass model inference to prevent unreliable predictions.
