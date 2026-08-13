"""
HemoVision Backend Service — Synthetic Presets for Live Judge Demonstration
"""

import base64
import numpy as np
import cv2
from typing import List
from backend.app.api.schemas import PresetDemoSample


class PresetService:
    """Generates synthetic preset images for 1-click demonstration to judges."""

    @staticmethod
    def get_presets() -> List[PresetDemoSample]:
        def create_synthetic_eye(r_val: int, g_val: int, b_val: int, blur: bool = False) -> str:
            h, w = 240, 320
            img = np.zeros((h, w, 3), dtype=np.uint8)
            # Skin background
            img[:, :] = [210, 175, 155]
            # Sclera white region
            cv2.ellipse(img, (160, 100), (90, 45), 0, 0, 360, (240, 240, 245), -1)
            # Iris
            cv2.circle(img, (160, 100), 25, (60, 40, 30), -1)
            # Pupil
            cv2.circle(img, (160, 100), 10, (10, 10, 10), -1)
            # Palpebral conjunctiva inner lower eyelid red patch
            cv2.ellipse(img, (160, 155), (80, 20), 0, 0, 180, (r_val, g_val, b_val), -1)

            if blur:
                img = cv2.GaussianBlur(img, (21, 21), 0)
            else:
                # Add texture
                noise = np.random.randint(-5, 5, (h, w, 3), dtype=np.int16)
                img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

            bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            _, buf = cv2.imencode(".jpg", bgr)
            return base64.b64encode(buf).decode("utf-8")

        demo_a = PresetDemoSample(
            id="preset-normal",
            name="DEMO MODE: Synthetic Preset A (Normal Hb ~13.5 g/dL)",
            description="Synthetic conjunctiva image with rich vascular redness (R=225, G=65, B=75). Synthetic test only.",
            expected_hb_g_dl=13.5,
            expected_status="usable",
            image_b64=create_synthetic_eye(225, 65, 75, blur=False)
        )

        demo_b = PresetDemoSample(
            id="preset-mild",
            name="DEMO MODE: Synthetic Preset B (Mild Anemia ~11.2 g/dL)",
            description="Synthetic conjunctiva image with moderate paleness (R=210, G=95, B=100). Synthetic test only.",
            expected_hb_g_dl=11.2,
            expected_status="usable",
            image_b64=create_synthetic_eye(210, 95, 100, blur=False)
        )

        demo_c = PresetDemoSample(
            id="preset-severe",
            name="DEMO MODE: Synthetic Preset C (Severe Anemia ~7.5 g/dL)",
            description="Synthetic conjunctiva image with severe pallor (R=205, G=140, B=140). Synthetic test only.",
            expected_hb_g_dl=7.5,
            expected_status="usable",
            image_b64=create_synthetic_eye(205, 140, 140, blur=False)
        )

        demo_d = PresetDemoSample(
            id="preset-blurry",
            name="DEMO MODE: Synthetic Preset D (Quality Failure — Blurry)",
            description="Synthetic out-of-focus image designed to test Quality Gating rejection. Synthetic test only.",
            expected_hb_g_dl=None,
            expected_status="rejected_blur",
            image_b64=create_synthetic_eye(220, 70, 75, blur=True)
        )

        return [demo_a, demo_b, demo_c, demo_d]
