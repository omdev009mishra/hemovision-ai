# Laboratory reference collection SOP

The reference hemoglobin measurement must originate from the approved laboratory reference process. The research linkage record contains `lab_measurement_id`, pseudonymous `participant_id`, `Hb`, timestamp, measurement method, instrument, and quality flag.

The responsible laboratory process governs sample collection, analyzer quality control, result verification, and retention of original laboratory reports. Operators must not manually estimate Hb from images, and no model prediction may be used as ground truth.

`LabAligner` selects the closest valid approved laboratory measurement and records `image_timestamp`, `lab_timestamp`, `time_delta_minutes`, `selected_lab_measurement_id`, and `alignment_status` against the approved study alignment window.
