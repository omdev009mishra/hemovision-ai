"""
HemoVision FastAPI Server Main Entrypoint — Phase 9 & Phase 10
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.api.routes import router as api_router

app = FastAPI(
    title="HemoVision Medical AI Research API",
    description=(
        "Non-Invasive Anemia Screening & Hemoglobin Estimation Research System. "
        "INVESTIGATIONAL PROTOTYPE — NOT FOR CLINICAL DIAGNOSIS."
    ),
    version="v1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for local cross-origin web client and mobile access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API router
app.include_router(api_router)

# Mount Static Files for Demo Dashboard UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def read_root():
    """Serve the HemoVision Interactive Research Dashboard UI."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "HemoVision API running. Open /docs for OpenAPI documentation."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
