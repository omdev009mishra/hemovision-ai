# HemoVision Mobile Camera Selection & Multi-Lens Protocol

## 1. Camera Architecture & Selection
HemoVision supports both **Front** and **Rear/Back** smartphone cameras for conjunctival image acquisition.

## 2. Lens Handling Logic
- **Front Camera**: Used primarily for self-acquisition. Preview may be mirrored for user ergonomics, but saved research images maintain un-mirrored anatomical orientation.
- **Rear Camera Array**: On devices with multiple rear lenses (e.g. Wide, Ultrawide, Telephoto), HemoVision prioritizes the primary main wide lens (`main_wide`).

## 3. Metadata Recording
Every captured frame records:
- `camera_lens_direction`: `front`, `back`, or `unknown`
- `camera_lens_type`: `main_wide`, `ultra_wide`, `telephoto`, `front_facing`, or `unknown`
- `phone_manufacturer` and `phone_model`

## 4. Session Preservation
Switching cameras via the in-app `CameraSelector` toggle (`↻`) preserves the active `session_id`, `participant_id`, and `eye_side` state.
