import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure project root is importable when running from backend/ (uvicorn app:app).
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from backend.routes import router
except ModuleNotFoundError:
    # Supports running from backend/ with: uvicorn app:app
    from routes import router


app = FastAPI(
    title="AI Adaptive Onboarding Engine API",
    version="1.0.0",
    description="Resume and JD analysis with adaptive learning roadmap generation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
