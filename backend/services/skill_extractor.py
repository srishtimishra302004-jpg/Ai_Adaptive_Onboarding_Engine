import re
from typing import Any

from models.skill_taxonomy import SKILL_CATEGORIES, SKILL_SYNONYMS, ALL_SKILLS


class SkillExtractor:
    def __init__(self) -> None:
        self.level_patterns = {
            "advanced": [
                r"\boptimized\b",
                r"\barchitected\b",
                r"\bscaled\b",
                r"\blead\b",
                r"\bmentored\b",
                r"\bdeep learning pipelines?\b",
            ],
            "intermediate": [
                r"\bbuilt\b",
                r"\bdeveloped\b",
                r"\bimplemented\b",
                r"\bdeployed\b",
                r"\bintegrated\b",
            ],
            "beginner": [
                r"\bfamiliar with\b",
                r"\bbasics of\b",
                r"\bintro to\b",
                r"\blearned\b",
            ],
        }

    def _normalize(self, text: str) -> str:
        normalized = text.lower()
        for source, target in SKILL_SYNONYMS.items():
            normalized = re.sub(rf"\b{re.escape(source.lower())}\b", target.lower(), normalized)
        return normalized

    def _infer_level(self, text: str) -> str:
        for level in ("advanced", "intermediate", "beginner"):
            if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in self.level_patterns[level]):
                return level
        return "beginner"

    def extract_resume_skills(self, text: str) -> dict[str, Any]:
        normalized = self._normalize(text)
        skills: list[dict[str, str]] = []
        for skill in ALL_SKILLS:
            if re.search(rf"\b{re.escape(skill.lower())}\b", normalized):
                skills.append({"skill": skill, "level": self._infer_level(normalized)})
        return {"skills": skills}

    def extract_jd_skills(self, text: str) -> dict[str, Any]:
        normalized = self._normalize(text)
        skills: list[dict[str, str]] = []
        for skill in ALL_SKILLS:
            if re.search(rf"\b{re.escape(skill.lower())}\b", normalized):
                if "senior" in normalized or "expert" in normalized:
                    level = "advanced"
                elif "2+ years" in normalized or "3+ years" in normalized:
                    level = "intermediate"
                else:
                    level = "beginner"
                skills.append({"skill": skill, "level": level})
        return {"skills": skills}

    def category_for_skill(self, skill: str) -> str:
        for category, values in SKILL_CATEGORIES.items():
            if skill in values:
                return category
        return "Other"
