# Standardized Image Acquisition Protocol

This document defines the physical capture procedure, optical targets, lighting recording guidelines, and quality rejection criteria for acquiring palpebral conjunctiva photographs.

---

## 1. Camera Positioning & Optical Targets

To maintain reproducible image scale and optical resolution across operators:

* **Target Focal Distance**: Approximately **10 cm to 20 cm** from the smartphone camera lens to the ocular surface (subject to lens minimum focus distance).
* **Framing & Alignment**: The eye must occupy the central 50% of the camera viewfinder. The everted lower eyelid (palpebral conjunctiva) must be clearly visible and horizontally centered.
* **Camera Stability**: The operator should brace the camera hand or hold the smartphone firmly with both hands to minimize hand tremor motion blur.
* **Lens Selection**: Use the primary wide camera module (`main_wide`). Ultra-wide and front-facing selfie lenses should be avoided due to optical distortion and lower sensor resolution.

> *Note: Target distances and framing guides are initial target ranges that will be experimentally refined during Phase 2 camera prototyping.*

---

## 2. Lighting & Environmental Controls

Lighting variations alter tissue spectral reflectance. Every capture session must log lighting parameters:

### Lighting Categories
1. `indoor_ambient`: Indoor room lighting (fluorescent, LED, incandescent).
2. `indoor_led_flash`: Controlled smartphone LED flash pulse.
3. `outdoor_shade`: Natural daylight under outdoor shade or overcast sky.
4. `direct_sunlight`: Direct solar illumination (recorded for exclusion/subgroup analysis).
5. `controlled_light_box`: Specialized research light-shielding attachment.

### Measured Environmental Parameters
* **Ambient Lux (`ambient_lux`)**: Recorded in lux via ambient light sensor where supported.
* **Color Temperature (`color_temperature_kelvin`)**: Correlated color temperature in Kelvin.
* **Flash Setting**: Flash LED mode (`off`, `on_flash_pulse`, `continuous_torch`).

---

## 3. Multi-Frame Burst Eye Capture Procedure

1. **Eversion Technique**: Clinician or participant gently pulls down the lower eyelid using a clean gloved finger placed on the skin below the lower eyelash line, exposing the vascularized palpebral conjunctiva mucosa.
2. **Burst Acquisition**: Capture a burst of **3 to 5 consecutive frames** per eye.
3. **Left & Right Eye**: Repeat the procedure for both left eye (`left`) and right eye (`right`).
4. **Best-Frame Selection**: Automated focus and exposure scoring selects the highest-quality frame from the burst sequence for segmentation, retaining secondary frames for stability analysis.

---

## 4. Quality Rejection Criteria & Preservation

Images failing quality criteria must be tagged with explicit rejection reasons:

| Rejection Code | Description |
| :--- | :--- |
| `BLUR` | Severe motion blur or out-of-focus optics (`focus_score` below threshold). |
| `OVEREXPOSURE` | Specular glare or sensor saturation clipping pixels in palpebral mucosa (`exposure_status == "overexposed"`). |
| `UNDEREXPOSURE` | Insufficient light causing shadow darkness in palpebral mucosa (`exposure_status == "underexposed"`). |
| `CONJUNCTIVA_NOT_VISIBLE` | Inadequate eversion; palpebral mucosa not exposed. |
| `OCCLUSION` | Eyelashes, fingers, or tear film glare obstruct $> 25\%$ of palpebral mucosa. |
| `BAD_FRAMING` | Palpebral conjunctiva cropped out of image frame boundary. |
| `MOTION` | Subject eye movement or blink during exposure. |
| `REFLECTION` | Severe specular reflection highlight across central mucosa. |
| `OTHER` | Unclassified artifact rendering image unanalyzable. |

> [!IMPORTANT]
> **REJECTED IMAGE PRESERVATION**: During research development, images flagged for quality rejection **MUST NOT** be automatically deleted. Their metadata, quality scores, and rejection codes are preserved in secure research storage for evaluating quality gate thresholds and training automated rejection models.
