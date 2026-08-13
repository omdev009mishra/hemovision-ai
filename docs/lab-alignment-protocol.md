# HemoVision — Laboratory Reference Alignment Protocol

## 1. Principle
Ground-truth hemoglobin ($g/dL$) values must originate strictly from accredited laboratory hematology analyzer reference measurements. Inferred, estimated, or manually entered values are strictly prohibited.

---

## 2. Temporal Alignment Window

To minimize physiological fluctuations, image capture and blood sampling must occur within a tight protocol window:

- **Maximum Allowed Time Delta ($\Delta t$)**: Configurable via `maximum_delta_minutes` (Default: $\le 120 \text{ minutes}$).
- **Formula**:
  $$\Delta t = \frac{|\text{Timestamp}_{\text{Image}} - \text{Timestamp}_{\text{Lab}}|}{60} \text{ (Minutes)}$$

If $\Delta t > \text{maximum\_delta\_minutes}$, the record is flagged as `alignment_status: "outside_protocol"` and excluded from ML model training sets.

---

## 3. Multiple Laboratory Measurements Resolution

When a participant undergoes multiple laboratory blood draws, `LabAligner` selects the measurement with the **minimum absolute time delta $|\Delta t|$** relative to image capture.
