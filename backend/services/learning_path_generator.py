from __future__ import annotations

from typing import Any

from models.adaptive_algorithm import AdaptiveRoadmapEngine


class LearningPathGenerator:
    def __init__(self) -> None:
        self.engine = AdaptiveRoadmapEngine()

    def generate(self, analysis: dict[str, Any], career_goal: str) -> dict[str, Any]:
        skill_gap = analysis["skill_gap"]
        required = analysis["required_skills"]
        user_skills = analysis["user_skills"]

        # Critical fix: always generate a path, even when no skill gaps exist.
        core_items = self.engine.generate(skill_gap[:4], career_goal) if skill_gap else []
        if not core_items:
            core_seed = required[:2] or user_skills[:2]
            core_items = self.engine.generate(core_seed, career_goal)

        advanced_seed = [s for s in (required + user_skills) if s not in skill_gap][:3] or required[:3] or user_skills[:3]
        advanced_items = self.engine.advanced_path(advanced_seed, career_goal)

        readiness_seed = ["Git", "Docker", "AWS"]
        readiness_items = self.engine.generate(readiness_seed, f"{career_goal} with industry readiness")

        path = [
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
                "why": "Strengthen production engineering, deployment, and delivery confidence.",
                "resources": [r for i in readiness_items for r in i.get("resources", [])][:6],
            },
        ]

        reasoning = (
            "Roadmap is grouped by immediate gap closure, depth specialization, and practical production readiness."
        )
        missing_skill_explanation = (
            "You meet all required skills. Focus on depth, tooling maturity, and measurable production outcomes."
            if not skill_gap
            else f"Missing or under-leveled skills detected: {', '.join(skill_gap)}."
        )
        recommendations = [res for track in path for res in track["resources"]]
        return {
            "learning_path": path,
            "recommendations": recommendations[:5],
            "reasoning": reasoning,
            "missing_skill_explanation": missing_skill_explanation,
        }
