import re
from models.skill_taxonomy import SKILL_CATEGORIES, SKILL_SYNONYMS, ALL_SKILLS

LEVEL_PATTERNS = {
    "advanced": [r"\boptimized\b", r"\barchitected\b", r"\bscaled\b", r"\blead\b", r"\bmentored\b"],
    "intermediate": [r"\bbuilt\b", r"\bdeveloped\b", r"\bimplemented\b", r"\bdeployed\b", r"\bintegrated\b"],
    "beginner": [r"\bfamiliar with\b", r"\bbasics of\b", r"\blearned\b"],
}


class SkillExtractor:
    def _normalize(self, text: str) -> str:
        text = text.lower()
        for src, tgt in SKILL_SYNONYMS.items():
            text = re.sub(rf"\b{re.escape(src.lower())}\b", tgt.lower(), text)
        return text

    def _infer_level(self, text: str) -> str:
        for level, patterns in LEVEL_PATTERNS.items():
            if any(re.search(p, text, re.IGNORECASE) for p in patterns):
                return level
        return "beginner"

    def extract_resume_skills(self, text: str) -> dict:
        normalized = self._normalize(text)
        return {"skills": [
            {"skill": skill, "level": self._infer_level(normalized)}
            for skill in ALL_SKILLS
            if re.search(rf"\b{re.escape(skill.lower())}\b", normalized)
        ]}

    def extract_jd_skills(self, text: str) -> dict:
        normalized = self._normalize(text)
        level = "advanced" if "senior" in normalized or "expert" in normalized else \
                "intermediate" if "2+ years" in normalized or "3+ years" in normalized else "beginner"
        return {"skills": [
            {"skill": skill, "level": level}
            for skill in ALL_SKILLS
            if re.search(rf"\b{re.escape(skill.lower())}\b", normalized)
        ]}

    def category_for_skill(self, skill: str) -> str:
        for category, values in SKILL_CATEGORIES.items():
            if skill in values:
                return category
        return "Other"
