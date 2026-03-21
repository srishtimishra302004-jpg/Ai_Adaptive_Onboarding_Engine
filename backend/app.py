from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router

app = FastAPI(
    title="AI Adaptive Onboarding Engine API",
    version="1.0.0",
    description="Resume and JD analysis with adaptive learning roadmap generation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "API is running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}