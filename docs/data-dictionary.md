# HemoVision Data Dictionary (Phase 1 Specification)

This document serves as the authoritative Data Dictionary for the HemoVision research dataset contract.

---

## Privacy Sensitivity Classifications

* **`PUBLIC`**: Non-identifiable metadata, standard enumerations, schema versions.
* **`INTERNAL`**: Study-generated pseudonymous keys, operator IDs, device IDs, protocol flags.
* **`SENSITIVE`**: Demographic summaries, altitude, general environmental parameters.
* **`HIGHLY_SENSITIVE`**: Protected Health Information (PHI), raw laboratory blood measurements, precise clinical timestamps. Must NEVER be committed to Git or public repositories.

---

## 1. Participant Fields

| Field Name | Entity | Data Type | Required | Allowed Values / Range | Units | Description | Source | Privacy Sensitivity | Usage | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `participant_id` | Participant | `string` | **Yes** | Pattern: `^[A-Za-z0-9_-]{3,64}$` | N/A | Unique pseudonymous participant key. | Study Admin | `INTERNAL` | Split Unit / Linkage | Never use real name or hospital ID. |
| `age_years` | Participant | `integer` | **Yes** | `0` to `120` | Years | Participant age in completed years. | Self-report / EHR | `SENSITIVE` | Feature / Bias Audit | Confounder for baseline Hb. |
| `sex` | Participant | `string` | **Yes** | `male`, `female`, `intersex`, `unknown` | N/A | Biological sex assigned at birth. | Self-report / EHR | `SENSITIVE` | Feature / Stratification | Confounder for baseline Hb. |
| `pregnancy_status` | Participant | `string` | **Yes** | `not_pregnant`, `first_trimester`, `second_trimester`, `third_trimester`, `postpartum`, `not_applicable`, `unknown` | N/A | Pregnancy state or trimester. | Clinical Interview | `HIGHLY_SENSITIVE` | Stratification / Subgroup | Plasma volume expansion alters Hb. |
| `smoking_status` | Participant | `string` | **Yes** | `never`, `active_smoker`, `former_smoker`, `unknown` | N/A | Tobacco smoking status. | Clinical Interview | `SENSITIVE` | Feature / Subgroup | Carboxyhemoglobin elevates Hb. |
| `skin_phototype` | Participant | `string` | Optional | `I`, `II`, `III`, `IV`, `V`, `VI`, `unknown` | N/A | Fitzpatrick skin phototype scale. | Clinical Assessment | `SENSITIVE` | Bias Audit / Subgroup | Evaluates fairness across skin tones. |
| `residence_altitude_m` | Participant | `number` | Optional | `0.0` to `9000.0` | Meters | Altitude of primary residence. | Geographic Data | `SENSITIVE` | Feature / Correction | High altitude induces erythropoiesis. |
| `relevant_comorbidities` | Participant | `array[string]`| Optional | String array | N/A | Reported systemic health conditions. | EHR / Interview | `HIGHLY_SENSITIVE` | Subgroup Audit | e.g. CKD, sickle cell, malaria. |
| `relevant_ocular_conditions`| Participant | `array[string]`| Optional | String array | N/A | Ocular conditions affecting conjunctiva. | Eye Exam | `HIGHLY_SENSITIVE` | Exclusion / Subgroup | e.g. conjunctivitis, pterygium. |

---

## 2. Capture Session Fields

| Field Name | Entity | Data Type | Required | Allowed Values / Range | Units | Description | Source | Privacy Sensitivity | Usage | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `session_id` | Session | `string` | **Yes** | Pattern: `^[A-Za-z0-9_-]{3,64}$` | N/A | Unique capture session identifier. | App Generated | `INTERNAL` | Grouping / Linkage | Groups images taken at same time. |
| `participant_id` | Session | `string` | **Yes** | Foreign Key $\rightarrow$ `Participant` | N/A | Linkage key to participant. | App Generated | `INTERNAL` | Linkage | Required for referential integrity. |
| `session_timestamp` | Session | `string` | **Yes** | ISO 8601 Date-Time | N/A | Timestamp of session start. | App System Clock | `HIGHLY_SENSITIVE` | Time-Delta Calculation | Used to compute time to lab draw. |
| `operator_id` | Session | `string` | **Yes** | Pattern: `^[A-Za-z0-9_-]{3,64}$` | N/A | Pseudonymous clinician / operator ID. | App Login | `INTERNAL` | Inter-operator Bias | Evaluates operator variation. |
| `capture_environment` | Session | `string` | **Yes** | `clinical_room`, `field_clinic`, `household`, `outdoor`, `unknown` | N/A | Physical setting of capture. | Operator Selection| `INTERNAL` | Subgroup / Evaluation | Environmental subgroup analysis. |
| `lighting_condition` | Session | `string` | **Yes** | `indoor_ambient`, `indoor_led_flash`, `outdoor_shade`, `direct_sunlight`, `controlled_light_box`, `unknown` | N/A | Primary illumination category. | App / Sensor | `INTERNAL` | Feature / Stratification | Critical for color calibration. |
| `ambient_lux` | Session | `number` | Optional | $\ge 0.0$ | Lux | Ambient illuminance level. | Device Sensor | `INTERNAL` | Quality Control / Feature | Recorded if sensor available. |
| `color_temperature_kelvin`| Session | `number` | Optional | `1000.0` to `15000.0` | Kelvin | Light source color temperature. | Calculated / Sensor | `INTERNAL` | Color Normalization | Used in ISP correction. |
| `device_id` | Session | `string` | **Yes** | Pattern: `^[A-Za-z0-9_-]{3,64}$` | N/A | Pseudonymous study device ID. | App Config | `INTERNAL` | Device Bias Audit | Never use IMEI or hardware MAC. |
| `consent_status` | Session | `string` | **Yes** | `verified_active`, `withdrawn`, `pending` | N/A | Participant consent verification. | Consent System | `SENSITIVE` | Inclusion Gate | `withdrawn` sessions are excluded. |

---

## 3. Image Fields

| Field Name | Entity | Data Type | Required | Allowed Values / Range | Units | Description | Source | Privacy Sensitivity | Usage | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `image_id` | Image | `string` | **Yes** | Pattern: `^[A-Za-z0-9_-]{3,64}$` | N/A | Unique image record identifier. | App Generated | `INTERNAL` | Primary Key | Identifies image file. |
| `session_id` | Image | `string` | **Yes** | Foreign Key $\rightarrow$ `Session` | N/A | Session linkage key. | App Generated | `INTERNAL` | Linkage | Foreign key to session. |
| `participant_id` | Image | `string` | **Yes** | Foreign Key $\rightarrow$ `Participant` | N/A | Participant linkage key. | App Generated | `INTERNAL` | Data Split Isolation | Used for split enforcement. |
| `eye_side` | Image | `string` | **Yes** | `left`, `right`, `unknown` | N/A | Anatomical eye side. | Operator Selection| `PUBLIC` | Feature / Pair Analysis | Allows left/right comparison. |
| `frame_index` | Image | `integer` | **Yes** | $\ge 0$ | Index | Burst frame sequence number. | Camera API | `PUBLIC` | Burst Selection | Selects best frame in sequence. |
| `image_path` | Image | `string` | **Yes** | Relative URI string | N/A | Relative storage path. | Storage Engine | `INTERNAL` | Data Loader | Points to secure storage path. |
| `capture_timestamp` | Image | `string` | **Yes** | ISO 8601 Date-Time | N/A | Image frame capture timestamp. | Camera Metadata | `HIGHLY_SENSITIVE` | Alignment | Exact frame timestamp. |
| `phone_manufacturer` | Image | `string` | **Yes** | Free text (e.g. `Google`) | N/A | Smartphone manufacturer name. | EXIF / System API| `PUBLIC` | Camera Bias Audit | Hardware stratification. |
| `phone_model` | Image | `string` | **Yes** | Free text (e.g. `Pixel 7 Pro`) | N/A | Smartphone model identifier. | EXIF / System API| `PUBLIC` | Camera Bias Audit | Sensor / ISP stratification. |
| `camera_lens_type` | Image | `string` | **Yes** | `main_wide`, `telephoto`, `ultra_wide`, `front_facing`, `unknown` | N/A | Camera lens module used. | Camera API | `PUBLIC` | Feature / Filtering | Standardizes focal length. |
| `image_width` | Image | `integer` | **Yes** | $\ge 1$ | Pixels | Image pixel width. | Image Header | `PUBLIC` | Preprocessing | Dimension check. |
| `image_height` | Image | `integer` | **Yes** | $\ge 1$ | Pixels | Image pixel height. | Image Header | `PUBLIC` | Preprocessing | Dimension check. |
| `focus_score` | Image | `number` | **Yes** | $\ge 0.0$ | Variance | Sharpness metric (Laplacian var). | Quality Engine | `PUBLIC` | Quality Gate | Rejects blurred images. |
| `exposure_info` | Image | `object` | **Yes** | Nested JSON object | N/A | Intensity & clipping ratios. | Quality Engine | `PUBLIC` | Quality Gate | Rejects over/underexposed photos.|
| `image_quality_status` | Image | `string` | **Yes** | `usable`, `rejected_blur`, `rejected_exposure`, `rejected_occlusion`, `rejected_framing`, `pending_review` | N/A | Quality decision state. | Quality Engine | `INTERNAL` | Dataset Filter | Only `usable` images enter training. |
| `annotation_status` | Image | `string` | **Yes** | `unannotated`, `in_review`, `annotated`, `rejected_quality` | N/A | ROI annotation state. | Annotation System| `INTERNAL` | Pipeline Gate | Tracks segmentation progress. |

---

## 4. Laboratory Measurement Fields

| Field Name | Entity | Data Type | Required | Allowed Values / Range | Units | Description | Source | Privacy Sensitivity | Usage | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `lab_measurement_id` | Lab | `string` | **Yes** | Pattern: `^[A-Za-z0-9_-]{3,64}$` | N/A | Unique lab record identifier. | Lab System / EHR | `INTERNAL` | Primary Key | Primary key for lab record. |
| `participant_id` | Lab | `string` | **Yes** | Foreign Key $\rightarrow$ `Participant` | N/A | Participant linkage key. | Lab System / EHR | `INTERNAL` | Linkage | Foreign key to participant. |
| `measurement_timestamp` | Lab | `string` | **Yes** | ISO 8601 Date-Time | N/A | Blood draw timestamp. | Phlebotomy Record | `HIGHLY_SENSITIVE` | Time-Delta Calculation | Used to compute `time_delta_minutes`.|
| `laboratory_hb_g_dl` | Lab | `number` | **Yes** | `2.0` to `25.0` | g/dL | Reference hemoglobin level. | Lab Analyzer | `HIGHLY_SENSITIVE` | ML Regression Target | Primary clinical ground truth. |
| `measurement_method` | Lab | `string` | **Yes** | `venous_automated_hematology`, `capillary_microcuvette`, `cyanmethemoglobin_reference`, `other_validated_method` | N/A | Analytical reference method. | Lab Spec | `INTERNAL` | Ground Truth Category | Stratifies lab accuracy. |
| `instrument_manufacturer`| Lab | `string` | **Yes** | Free text (e.g. `Sysmex`) | N/A | Hematology analyzer maker. | Lab Spec | `INTERNAL` | Instrument Audit | Analyzer hardware vendor. |
| `instrument_model` | Lab | `string` | **Yes** | Free text (e.g. `XN-1000`) | N/A | Hematology analyzer model. | Lab Spec | `INTERNAL` | Instrument Audit | Analyzer model number. |
| `hematocrit_pct` | Lab | `number` | Optional | `5.0` to `75.0` | % | Volume percentage of RBCs. | Lab Analyzer | `HIGHLY_SENSITIVE` | Secondary Ground Truth | Recorded if CBC available. |
| `rbc_count_10e6_uL` | Lab | `number` | Optional | `0.5` to `10.0` | $10^6/\mu\text{L}$ | RBC count per microliter. | Lab Analyzer | `HIGHLY_SENSITIVE` | Secondary Ground Truth | Recorded if CBC available. |
| `lab_quality_status` | Lab | `string` | **Yes** | `valid_verified`, `hemolyzed_sample`, `clotted_sample`, `unverified_flag` | N/A | Sample validity status. | Lab Tech Review | `INTERNAL` | Quality Filter | Non-valid samples excluded. |

---

## 5. Annotation Fields

| Field Name | Entity | Data Type | Required | Allowed Values / Range | Units | Description | Source | Privacy Sensitivity | Usage | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `annotation_id` | Annotation| `string` | **Yes** | Pattern: `^[A-Za-z0-9_-]{3,64}$` | N/A | Unique annotation record key. | Annotation Tool | `INTERNAL` | Primary Key | Identifies mask record. |
| `image_id` | Annotation| `string` | **Yes** | Foreign Key $\rightarrow$ `Image` | N/A | Image linkage key. | Annotation Tool | `INTERNAL` | Linkage | Foreign key to image. |
| `annotator_id` | Annotation| `string` | **Yes** | Pattern: `^[A-Za-z0-9_-]{3,64}$` | N/A | Pseudonymous annotator ID. | User Auth | `INTERNAL` | Inter-annotator Audit | Tracks expert agreement. |
| `annotation_version` | Annotation| `string` | **Yes** | SemVer pattern `^v[0-9]+\.[0-9]+\.[0-9]+$` | N/A | Annotation tool/spec version. | Annotation Tool | `PUBLIC` | Version Tracking | Ensures spec reproducibility. |
| `conjunctiva_mask_path` | Annotation| `string` | **Yes** | Relative URI string | N/A | Path to segmentation mask. | Annotation System| `INTERNAL` | ML Segmentation Target | Target for U-Net training. |
| `quality_label` | Annotation| `string` | **Yes** | `high_quality`, `acceptable`, `poor_quality`, `unusable` | N/A | Visual tissue clarity score. | Expert Reviewer | `INTERNAL` | Quality Weighting | Weights loss functions. |
| `occlusion_label` | Annotation| `string` | **Yes** | `none`, `finger_occlusion`, `eyelash_occlusion`, `specular_reflection`, `multiple_occlusions` | N/A | Obstruction type present. | Expert Reviewer | `INTERNAL` | Quality Filtering | Identifies visual artifacts. |
| `annotation_status` | Annotation| `string` | **Yes** | `draft`, `submitted`, `approved`, `rejected` | N/A | Annotation workflow state. | Workflow System | `INTERNAL` | Dataset Ingestion Gate | Only `approved` masks used. |
| `review_status` | Annotation| `string` | **Yes** | `pending_peer_review`, `peer_reviewed_approved`, `peer_reviewed_rejected` | N/A | Clinical review verification. | Lead Clinician | `INTERNAL` | Quality Assurance | Peer review sign-off. |
