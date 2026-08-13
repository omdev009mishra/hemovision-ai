# Laboratory Ground Truth Reference Protocol

This document defines the protocol for acquiring, validating, and linking clinical reference laboratory hemoglobin (Hb) measurements to conjunctival image capture sessions.

---

## 1. Reference Target & Analytical Methods

The **Clinical Ground Truth reference target** for predictive modeling is systemic hemoglobin concentration expressed in grams per deciliter (**g/dL**), recorded as `laboratory_hb_g_dl`.

### Analytical Reference Methods
The clinical study protocol specifies the approved reference method:
1. `venous_automated_hematology`: Venous blood draw analyzed on an automated hematology analyzer (e.g., Sysmex XN-series, Beckman Coulter DxH-series).
2. `capillary_microcuvette`: Capillary blood microcuvette photometry (e.g., HemoCue 201+ / 801).
3. `cyanmethemoglobin_reference`: International Council for Standardization in Haematology (ICSH) cyanmethemoglobin reference spectrophotometry.
4. `other_validated_method`: Alternative method documented in institutional study protocol.

> *No single analyzer is assumed to be universally superior. The specific instrument manufacturer (`instrument_manufacturer`) and model (`instrument_model`) must be explicitly logged for every record.*

---

## 2. Temporal Linkage & Time Delta Calculation

Systemic hemoglobin levels fluctuate due to fluid shifts, posture changes, blood loss, or fluid administration. 

To evaluate temporal stability:
* The exact timestamp of blood collection (`measurement_timestamp`) and exact timestamp of image acquisition (`capture_timestamp`) are recorded in ISO 8601 format.
* The absolute time difference in minutes is calculated for every image-reference pair:
  $$\text{time\_delta\_minutes} = \frac{|\text{capture\_timestamp} - \text{measurement\_timestamp}|}{60 \text{ seconds}}$$

> [!NOTE]
> ### Temporal Window Flexibility
> **HemoVision DOES NOT enforce a hardcoded universal 60-minute cutoff.**
> Instead, `time_delta_minutes` is continuously logged as a continuous variable. The effect of varying time deltas (e.g. 15 min, 30 min, 60 min, 120 min) on model prediction performance will be systematically evaluated through protocol sensitivity analysis.

---

## 3. Laboratory Quality Verification

Laboratory reference records must pass clinical quality checks before linkage:
* `lab_quality_status == "valid_verified"`: Sample verified by laboratory technician with no analyzer error flags.
* **Exclusion Flags**: Samples flagged as hemolyzed (`hemolyzed_sample`), clotted (`clotted_sample`), or unverified are excluded from model training datasets.
