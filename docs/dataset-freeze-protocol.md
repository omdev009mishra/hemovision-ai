# Dataset-freeze protocol

Freeze status begins as `OPEN`, may move to `UNDER_REVIEW`, then `FROZEN`, and may be `RELEASED_FOR_RESEARCH` only through an authorized institution-controlled workflow. The code rejects unauthorized transitions and does not mark a dataset clinically validated.

Before freeze, validate governance, active consent, schema conformance, duplicate image IDs, PII, EXIF privacy, image quality, segmentation status, lab alignment, withdrawal status, and participant-level split isolation. Rejected, failed-segmentation, unaligned, and withdrawn records are reported explicitly and excluded from the research-ready subset. Reports are written to `research/reports/freeze/` without participant-level data.
