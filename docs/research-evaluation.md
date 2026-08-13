# HemoVision Research Evaluation & Subgroup Protocol

## Evaluation Metrics
- **Mean Absolute Error (MAE)**: Continuous error in g/dL.
- **Root Mean Squared Error (RMSE)**: Penalizes larger estimation errors.
- **Coefficient of Determination ($R^2$)**: Variance explained by features.
- **Correlation**: Pearson $r$ and Spearman $\rho$.

## Conformal Uncertainty Quantification
- 95% empirical prediction intervals are calculated via residual calibration on validation data.
- Interval coverage and mean width are evaluated.

## Subgroup Analysis
Performance is evaluated across:
1. `camera_lens_direction` (`front` vs `back`)
2. `phone_manufacturer` & `phone_model`
3. `lighting_condition` & `capture_environment`
4. `age` & `sex`
