# Pilot study plan — research template

The pilot evaluates acquisition feasibility, image quality, segmentation success, operator workflow, metadata completeness, laboratory linkage success, failure rate, and processing time. It must not be used to claim Hb-model accuracy, diagnosis, or clinical validation.

Report these operational outputs:

- `capture_success_rate`
- `usable_image_rate`
- `segmentation_success_rate`
- `lab_linkage_rate`
- `metadata_completeness`
- `median_capture_time`
- `median_processing_time`

If the approved pilot participant count is insufficient for a performance analysis, report `INSUFFICIENT_DATA_FOR_PERFORMANCE_ESTIMATION`.

Before a pilot dataset is frozen, run governance, consent, schema, duplicate, PII, EXIF, quality, segmentation, alignment, withdrawal, and participant-level split checks. A freeze is an integrity state—not clinical validation.
