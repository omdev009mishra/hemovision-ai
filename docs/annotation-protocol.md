# Annotation Protocol

This specification defines the annotation guidelines, polygon boundary criteria, and quality categorization tags for creating conjunctiva segmentation datasets.

---

## 1. Anatomical Regions of Interest (ROI)

Annotators will mark three concentric spatial entities using polygon annotations:

```text
┌────────────────────────────────────────────────────────┐
│ Eye Bounding Box (Entire ocular region + orbit)       │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Lower Eyelid Region (Everted lid tissue)        │  │
│  │   ┌──────────────────────────────────────────┐   │  │
│  │   │ Palpebral Conjunctiva Mask (Target ROI) │   │  │
│  │   └──────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

### Region Definitions
1. **Eye Region**: Bounding box encompassing upper lid, lower lid, iris, and sclera.
2. **Lower Eyelid**: Polygon bounding the everted (pulled-down) lower eyelid tissue.
3. **Palpebral Conjunctiva (Target Mask)**: The palpebral conjunctiva is the vascularized, reddish mucous membrane lining the inner surface of the lower eyelid.
   * **Include**: Palpebral mucosa and fornix mucosa showing active microvascular capillaries.
   * **Exclude**: Bulbar conjunctiva (covering sclera), cornea, iris, mucocutaneous junction, eyelashes, outer skin, specular reflection highlights, and obscuring fingers pulling the lid.

---

## 2. Image Quality & Artifact Annotation Schema

Each image must be tagged with discrete quality ratings prior to segmentation:

| Quality Flag | Values | Description |
| :--- | :--- | :--- |
| `blur_score` | `none`, `mild`, `severe` | Motion blur or lens misfocus obscuring capillary patterns. |
| `exposure_status` | `optimal`, `overexposed`, `underexposed` | Specular blowout or shadow darkness in palpebral ROI. |
| `occlusion_level` | `none`, `finger_occlusion`, `lash_occlusion` | Degree to which fingers or eyelashes obstruct the palpebral mucosa. |
| `everts_adequacy` | `adequate`, `partial`, `inadequate` | Extent to which lower lid is fully pulled down to reveal palpebral tissue. |
| `usable_for_ml` | `boolean` (`true` / `false`) | Master decision flag indicating if image passes minimum quality gates. |

---

## 3. Annotation Format Standard

Annotations are exported in COCO-compliant JSON structure:

```json
{
  "image_id": "HV-IMG-001042-L",
  "annotations": [
    {
      "id": 1,
      "category": "palpebral_conjunctiva",
      "segmentation": [[120, 340, 145, 342, 190, 355, 230, 360, 210, 380, 150, 375]],
      "area": 4250.5,
      "bbox": [120, 340, 110, 40]
    }
  ],
  "quality_metadata": {
    "blur_score": "none",
    "exposure_status": "optimal",
    "occlusion_level": "none",
    "everts_adequacy": "adequate",
    "usable_for_ml": true
  }
}
```
