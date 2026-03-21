import sys
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 👉 FIX: add PROJECT ROOT (parent of backend)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 👉 Always use full import
from backend.routes import router


app = FastAPI(
    title="AI Adaptive Onboarding Engine API",
    version="1.0.0",
    description="Resume and JD analysis with adaptive learning roadmap generation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "API running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=True)