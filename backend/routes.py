from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from backend.services.gap_analyzer import GapAnalyzer
from backend.services.skill_extractor import SkillExtractor
from backend.utils.file_handler import extract_text
from models.adaptive_algorithm import AdaptiveRoadmapEngine

router = APIRouter()

skill_extractor = SkillExtractor()
gap_analyzer = GapAnalyzer()
engine = AdaptiveRoadmapEngine()

STATE = {"resume_text": "", "jd_text": ""}


class AnalyzeRequest(BaseModel):
    career_goal: str = "Become stronger for target role"


class AnalyzeTextRequest(BaseModel):
    resume_text: str
    jd_text: str
    career_goal: str = "Become stronger for target role"


def build_roadmap(analysis: dict, career_goal: str) -> list:
    skill_gap = analysis["skill_gap"]
    required = analysis["required_skills"]
    user_skills = analysis["user_skills"]

    core_seed = skill_gap[:4] or required[:2] or user_skills[:2]
    core_items = engine.generate(core_seed, career_goal)

    advanced_seed = [s for s in required + user_skills if s not in skill_gap][:3] or required[:3]
    advanced_items = engine.advanced_path(advanced_seed, career_goal)

    readiness_items = engine.generate(["Git", "Docker", "AWS"], f"{career_goal} with industry readiness")

    return [
        {
            "track": "Core Improvement",
            "what_to_learn": [i["skill"] for i in core_items],
            "why": "Close mandatory gaps and build role baseline quickly.",
            "resources": [r for i in core_items for r in i.get("resources", [])][:6],
        },
        {
            "track": "Advanced Specialization",
            "what_to_learn": [i["skill"] for i in advanced_items],
            "why": "Deepen specialization for higher-impact ownership.",
            "resources": [r for i in advanced_items for r in i.get("resources", [])][:6],
        },
        {
            "track": "Industry Readiness",
            "what_to_learn": [i["skill"] for i in readiness_items],
            "why": "Strengthen production engineering and deployment confidence.",
            "resources": [r for i in readiness_items for r in i.get("resources", [])][:6],
        },
    ]


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)) -> dict:
    STATE["resume_text"] = await extract_text(file)
    return {"message": "Upload successful", "chars": len(STATE["resume_text"])}


@router.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)) -> dict:
    STATE["jd_text"] = await extract_text(file)
    return {"message": "Upload successful", "chars": len(STATE["jd_text"])}


@router.post("/analyze")
def analyze(payload: AnalyzeRequest) -> dict:
    resume_profile = skill_extractor.extract_resume_skills(STATE["resume_text"].strip())
    jd_profile = skill_extractor.extract_jd_skills(STATE["jd_text"].strip())
    analysis = gap_analyzer.analyze(user_profile=resume_profile, required_profile=jd_profile)
    roadmap = build_roadmap(analysis, payload.career_goal)

    return {
        "scores": analysis["scores"],
        "skills": {
            "matched": analysis["matched_skills"],
            "missing": analysis["missing_skills"],
            "partial": analysis["partial_matches"],
            "categorized": analysis["skill_categories"],
        },
        "experience_level": analysis["experience_level"],
        "skill_strength": analysis["skill_strength"],
        "skill_gap_analysis": analysis["skill_gap_analysis"],
        "learning_roadmap": roadmap,
        "reasoning_trace": analysis["reasoning_trace"],
    }


@router.post("/analyze-text")
def analyze_text(payload: AnalyzeTextRequest) -> dict:
    STATE["resume_text"] = payload.resume_text
    STATE["jd_text"] = payload.jd_text
    return analyze(AnalyzeRequest(career_goal=payload.career_goal))


@router.get("/roadmap")
def get_roadmap() -> dict:
    return {"learning_path": STATE.get("roadmap", [])}
