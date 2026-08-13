# Image-quality review protocol

An authorized research operator independently reviews the capture-quality and ROI evidence and records:

- `reviewer_id` (pseudonymous)
- `review_timestamp`
- `review_reason`
- `review_status`: `ACCEPT`, `REJECT`, or `REVIEW`

Reviewers classify images; they do not modify laboratory Hb values. Quality review confirms, but does not override, the record that a segmentation failure is `REVIEW_REQUIRED` or that a rejected image has its recorded rejection reason. No review outcome authorizes diagnosis or clinical-model training.
