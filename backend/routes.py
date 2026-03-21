from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

try:
    from backend.services.gap_analyzer import GapAnalyzer
    from backend.services.jd_parser import JDParser
    from backend.services.learning_path_generator import LearningPathGenerator
    from backend.services.resume_parser import ResumeParser
    from backend.services.skill_extractor import SkillExtractor
    from backend.utils.file_handler import extract_text
except ModuleNotFoundError:
    # Supports running from backend/ with: uvicorn app:app
    from services.gap_analyzer import GapAnalyzer
    from services.jd_parser import JDParser
    from services.learning_path_generator import LearningPathGenerator
    from services.resume_parser import ResumeParser
    from services.skill_extractor import SkillExtractor
    from utils.file_handler import extract_text

router = APIRouter()

resume_parser = ResumeParser()
jd_parser = JDParser()
skill_extractor = SkillExtractor()
gap_analyzer = GapAnalyzer()
path_generator = LearningPathGenerator()

STATE = {
    "resume_text": "",
    "jd_text": "",
    "analysis": {},
    "roadmap": [],
}


class AnalyzeRequest(BaseModel):
    career_goal: str | None = "Become stronger for target role"


class AnalyzeTextRequest(BaseModel):
    resume_text: str
    jd_text: str
    career_goal: str | None = "Become stronger for target role"


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)) -> dict:
    text = await extract_text(file)
    STATE["resume_text"] = text
    return {"message": "Upload successful", "type": "resume", "chars": len(text)}


@router.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)) -> dict:
    text = await extract_text(file)
    STATE["jd_text"] = text
    return {"message": "Upload successful", "type": "jd", "chars": len(text)}


@router.post("/analyze")
def analyze(payload: AnalyzeRequest) -> dict:
    resume_text = resume_parser.parse(STATE["resume_text"])
    jd_text = jd_parser.parse(STATE["jd_text"])

    resume_profile = skill_extractor.extract_resume_skills(resume_text)
    jd_profile = skill_extractor.extract_jd_skills(jd_text)

    analysis = gap_analyzer.analyze(
        user_profile=resume_profile,
        required_profile=jd_profile,
    )

    roadmap = path_generator.generate(
        analysis=analysis,
        career_goal=payload.career_goal or "Career growth",
    )

    result = {
        "scores": {
            "resume_score": analysis["scores"]["resume_score"],
            "similarity_score": analysis["scores"]["similarity_score"],
            "ats_score": analysis["scores"]["ats_score"],
            "confidence_score": analysis["scores"]["confidence_score"],
        },
        "skills": {
            "matched": analysis["matched_skills"],
            "missing": analysis["missing_skills"],
            "partial": analysis["partial_matches"],
            "categorized": analysis["skill_categories"],
        },
        "experience_level": analysis["experience_level"],
        "skill_strength": analysis["skill_strength"],
        "skill_gap_analysis": analysis["skill_gap_analysis"],
        "learning_roadmap": roadmap["learning_path"],
        "reasoning_trace": analysis["reasoning_trace"],
    }

    STATE["analysis"] = result
    STATE["roadmap"] = roadmap["learning_path"]
    return result


@router.post("/analyze-text")
def analyze_text(payload: AnalyzeTextRequest) -> dict:
    STATE["resume_text"] = payload.resume_text
    STATE["jd_text"] = payload.jd_text
    return analyze(AnalyzeRequest(career_goal=payload.career_goal))


@router.get("/roadmap")
def get_roadmap() -> dict:
    return {"learning_path": STATE.get("roadmap", [])}
