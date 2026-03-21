from __future__ import annotations

import json
from pathlib import Path


class AdaptiveRoadmapEngine:
    def __init__(self) -> None:
        data_path = Path(__file__).parent / "learning_dataset.json"
        with data_path.open("r", encoding="utf-8") as f:
            self.dataset = json.load(f)

        self.dependencies = {
            "Deep Learning": ["Python", "Machine Learning"],
            "NLP": ["Python", "Machine Learning"],
            "FastAPI": ["Python"],
            "React": ["JavaScript"],
            "Data Analysis": ["Python", "SQL"],
        }

    def _lookup(self, skill: str, level: str) -> dict:
        for item in self.dataset:
            if item["skill"] == skill and item["level"] == level:
                return item
        for item in self.dataset:
            if item["skill"] == skill:
                return item
        return {"skill": skill, "level": level, "resources": ["https://roadmap.sh"]}

    def _topological_order(self, skills: list[str]) -> list[str]:
        ordered = []
        visited = set()

        def visit(skill: str) -> None:
            if skill in visited:
                return
            visited.add(skill)
            for dep in self.dependencies.get(skill, []):
                if dep in skills:
                    visit(dep)
            ordered.append(skill)

        for sk in skills:
            visit(sk)
        return ordered

    def generate(self, skill_gap: list[str], career_goal: str) -> list[dict]:
        ordered_skills = self._topological_order(skill_gap)
        path = []
        for idx, skill in enumerate(ordered_skills):
            level = "beginner" if idx == 0 else "intermediate"
            node = self._lookup(skill, level)
            node["why"] = f"Priority {idx + 1}: closes a role-critical gap for goal: {career_goal}."
            path.append(node)
        return path

    def advanced_path(self, skills: list[str], career_goal: str) -> list[dict]:
        path = []
        for idx, skill in enumerate(skills):
            node = self._lookup(skill, "advanced")
            node["why"] = (
                f"Advanced track {idx + 1}: strengthens specialization and leadership depth for goal: {career_goal}."
            )
            path.append(node)
        if not path:
            fallback = self._lookup("Machine Learning", "advanced")
            fallback["why"] = "General advanced upskilling path."
            path.append(fallback)
        return path
