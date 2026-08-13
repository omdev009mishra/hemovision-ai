# HemoVision Phase 2 — Smartphone Acquisition Prototype Architecture

> **RESEARCH DISCLAIMER**  
> HemoVision is developed exclusively for scientific investigation. The software and heuristics described herein are **EXPERIMENTAL** and **NOT CLINICALLY VALIDATED**. The system does not diagnose anemia, measure hemoglobin, or provide medical advice.

---

## 1. System Overview

Phase 2 introduces the Flutter mobile client (`hemovision_capture`) designed to capture high-quality palpebral conjunctiva images and produce schema-compliant metadata for ML dataset building.

```
mobile/hemovision_capture/
├── lib/
│   ├── app/
│   │   ├── app.dart                  # Root MaterialApp configuration
│   │   └── theme.dart                # Material 3 deep indigo theme
│   ├── core/
│   │   ├── constants.dart            # Schema enums and quality thresholds
│   │   ├── id_generator.dart         # UUID v4 and synthetic ID generators
│   │   ├── result.dart               # Type-safe Result<T> pattern
│   │   └── timestamp_utils.dart      # ISO 8601 UTC timestamp formatters
│   ├── models/
│   │   ├── capture_settings.dart     # Environment & lighting metadata
│   │   ├── exposure_info.dart        # Mean intensity & clipping ratios
│   │   ├── image_metadata.dart       # Schema-aligned image metadata model
│   │   ├── quality_result.dart       # On-device assessment results
│   │   └── session_metadata.dart     # Schema-aligned session metadata model
│   ├── services/
│   │   ├── camera_service.dart       # Camera package wrapper & burst capture
│   │   ├── device_info_service.dart  # Manufacturer & model identification
│   │   ├── metadata_service.dart     # Session & image metadata builder
│   │   ├── quality_engine.dart       # Laplacian focus & exposure heuristics
│   │   ├── sensor_service.dart       # Accelerometer motion stability monitor
│   │   └── storage_service.dart      # Local app-private filesystem storage
│   ├── widgets/
│   │   ├── alignment_reticle.dart    # Oval anatomical reticle CustomPainter
│   │   ├── environment_selector.dart # Environment & lighting choice chips
│   │   └── quality_indicator.dart    # Non-diagnostic quality badge
│   └── screens/
│       ├── home_screen.dart          # Session initialization screen
│       ├── capture_screen.dart       # Real-time camera preview & burst capture
│       ├── review_screen.dart        # Frame quality review & retake/accept
│       └── session_summary_screen.dart # Acquisition completion summary
└── test/
    └── widget_test.dart              # Unit & widget test suite
```

---

## 2. On-Device Quality Heuristics

All metrics produced by `QualityEngine` are engineering heuristics designed to filter unusable images prior to dataset insertion:

### Focus Score (Laplacian Variance)
- **Kernel:** 3x3 discrete Laplacian $[0, 1, 0; 1, -4, 1; 0, 1, 0]$ applied over grayscale pixels.
- **Metric:** Variance of the Laplacian convolution response $\text{Var}(\Delta I)$.
- **Threshold:** `kFocusScoreThreshold = 100.0` (unvalidated engineering heuristic).

### Exposure Analysis
- **Mean Pixel Intensity:** Mean luminance $\mu_I \in [0, 255]$.
- **Overexposure Ratio:** Fraction of pixels with intensity $> 240$.
- **Underexposure Ratio:** Fraction of pixels with intensity $< 15$.
- **Classification:** Overexposed if overexposed ratio $> 0.15$; Underexposed if underexposed ratio $> 0.15$.

### Frame Selection
Burst capture collects 3--5 frames. `selectBestFrame()` ranks candidate frames using a hierarchical rule:
$$\text{Usable Status} \succ \text{Highest Focus Score} \succ \text{Closest Mean Intensity to } 128$$

---

## 3. Data Flow & Storage

1. **Session Setup:** `HomeScreen` generates `sessionId` (UUID v4) and `participantId` (`HV-TEST-P-XXXXXXXX`).
2. **Acquisition:** `CaptureScreen` handles burst capture for Left Eye, then Right Eye.
3. **Quality Assessment:** `QualityEngine` processes decoded frame bytes on-device.
4. **Review:** `ReviewScreen` presents frame metrics and best-frame selection.
5. **Persistence:** `StorageService` writes to local application-private storage:
   ```
   app_documents/hemovision_data/sessions/{session_id}/
   ├── session_metadata.json
   ├── left_eye/
   │   ├── frame_000.jpg
   │   └── frame_000_metadata.json
   └── right_eye/
       ├── frame_000.jpg
       └── frame_000_metadata.json
   ```

---

## 4. Safety, Privacy & Regulatory Boundaries

- **No Medical Claims:** The prototype strictly presents physical image attributes (blur, exposure, stability) without medical terms.
- **No Remote Transmission:** All data remains on the physical device in app-private directories.
- **No PHI/PII:** Identifiers are synthetic or randomized UUIDs.
