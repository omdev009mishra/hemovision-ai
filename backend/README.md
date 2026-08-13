# HemoVision FastAPI Research Backend & Interactive Dashboard

The backend service provides FastAPI endpoints for image quality gating, palpebral conjunctiva ROI segmentation, feature extraction, ML hemoglobin estimation, conformal prediction intervals, 1-click synthetic judge demo presets, and clinical summary report generation.

---

## Directory Layout

```text
backend/
├── app/
│   ├── main.py                 # FastAPI application entrypoint & static file mounting
│   ├── api/
│   │   ├── routes.py           # API endpoints (/health, /analyze, /demo-samples, /reports/markdown)
│   │   └── schemas.py          # Pydantic V2 request & response schemas
│   ├── services/
│   │   ├── inference_service.py # ML InferencePipeline wrapper
│   │   ├── preset_service.py   # 1-Click synthetic demo preset generator
│   │   └── report_service.py   # Research summary report exporter
│   └── static/
│       └── index.html          # Interactive Judge Demo Dashboard UI
└── tests/
    └── test_backend_api.py     # FastAPI TestClient test suite
```

---

## Starting the Backend Server

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Interactive Research Dashboard UI**: Open [http://localhost:8000/](http://localhost:8000/) in your browser.
- **OpenAPI Interactive Documentation**: Open [http://localhost:8000/docs](http://localhost:8000/docs).

---

## API Endpoints

- `GET /api/v1/health`: System health status and safety boundary disclosure.
- `GET /api/v1/demo-samples`: Returns 4 1-click synthetic demo presets (Normal, Mild Anemia, Severe Anemia, Blurry Quality Reject).
- `POST /api/v1/analyze`: Accepts base64 encoded conjunctiva image JSON payload. Returns complete quality, segmentation, feature, prediction, and visual overlay.
- `POST /api/v1/analyze/file`: Accepts multipart file upload.
- `POST /api/v1/reports/markdown`: Generates downloadable Markdown research summary report.

---

## Running Backend Tests

```bash
$env:PYTHONPATH="d:\hemovision"; python -m pytest backend/tests/
```
