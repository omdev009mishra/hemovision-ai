# Clinical Requirements & Confounder Specifications

Future clinical validation of HemoVision requires rigorous tracking of physiological, environmental, and technological covariates that impact ocular reflectance, microvascular dynamics, and camera sensor capture.

---

## 1. Clinical Ground Truth

> [!IMPORTANT]
> ### Reference Target Definition
> **Laboratory Hemoglobin (Hb) Measurement** obtained via standard venous blood draw analyzed on an automated hematology analyzer (e.g., Sysmex, Beckman Coulter, or cyanmethemoglobin reference method) or validated point-of-care microcuvette system (e.g., HemoCue 201+) shall serve as the **Clinical Ground Truth reference target** for all predictive modeling and evaluation.

The reference dataset record must explicitly capture:
1. **Reference Method**: Exact instrument manufacturer and model.
2. **Timestamp of Blood Draw**: Precise date and time of sample collection.
3. **Timestamp of Image Capture**: Date and time of eye photo capture.
4. **Time Delta**: Absolute difference between blood draw and photograph (Target: $\le 60$ minutes to prevent physiological Hb shift due to fluid resuscitation, posture changes, or acute bleeding).

---

## 2. Mandatory Covariates & Confounding Factors

Model evaluation and dataset collection must capture and evaluate model bias across the following 13 factors:

### Physiological & Demographic Covariates
1. **Age**: Pediatric, adult, and geriatric microvascular differences.
2. **Sex**: Baseline physiological Hb distribution variations between males and females.
3. **Pregnancy Status**: Plasma volume expansion in pregnancy leads to physiological dilutional anemia.
4. **Smoking Status**: Heavy smoking elevates baseline carboxyhemoglobin and compensatory total Hb.
5. **Altitude**: Chronic high-altitude exposure induces compensatory erythropoiesis, raising normal Hb thresholds.
6. **Ethnicity & Skin Tone**: Evaluated using the Fitzpatrick Skin Phototype Scale (I–VI) and individual typography angle (ITA) to ensure zero algorithmic performance bias across diverse populations.
7. **Comorbidities & Ocular Conditions**: Jaundice/hyperbilirubinemia (scleral icterus), conjunctivitis, pinguecula, pterygium, dry eye syndrome, recent ocular surgery, or systemic vasodilation (fever/sepsis).

### Optical & Technological Covariates
8. **Smartphone Manufacturer & Sensor**: Differences in CMOS sensor spectral response curves (e.g., Sony IMX, Samsung ISOCELL).
9. **Camera Hardware Differences**: Lens aperture, optical image stabilization, raw sensor bit-depth.
10. **ISP (Image Signal Processor) Pipeline**: Automatic white balance (AWB), auto-exposure, gamma correction, noise reduction, and tone mapping algorithms inherent to iOS vs Android manufacturers.
11. **Lighting Conditions**: Ambient illuminance (lux), correlated color temperature (CCT in Kelvin), ambient vs flash LED illumination, direct sun glare, shadows.
12. **Image Quality Artifacts**: Motion blur, out-of-focus blur, specular reflections on tear film, shadow occlusion across lower lid.
13. **Operator Variation**: Variations in manual lower eyelid retraction force, lid eversion angle, and palpebral exposure area.
