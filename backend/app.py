import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROOT ROUTE (IMPORTANT)
@app.get("/")
def root():
    return {"status": "running"}

# ✅ SAFE ANALYZE ROUTE
@app.post("/analyze-text")
async def analyze_text(data: dict):
    return {
        "resume_score": 70,
        "similarity_score": 13,
        "ats_score": 80,
        "confidence_score": 76,
        "missing_skills": ["AWS"],
        "matched_skills": ["Python", "SQL", "ML"]
    }
