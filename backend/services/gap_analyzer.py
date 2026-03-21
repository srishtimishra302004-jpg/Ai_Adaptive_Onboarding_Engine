from __future__ import annotations

from typing import Any

import numpy as np

from models.matching_model import MatchingModel
from models.skill_taxonomy import SKILL_CATEGORIES


LEVEL_SCORE = {"beginner": 1, "intermediate": 2, "advanced": 3}


class GapAnalyzer:
    def __init__(self) -> None:
        self.matcher = MatchingModel()

    def _to_map(self, profile: dict[str, Any]) -> dict[str, str]:
        return {item["skill"]: item["level"] for item in profile.get("skills", [])}

    def _category_of(self, skill: str) -> str:
        for category, skills in SKILL_CATEGORIES.items():
            if skill in skills:
                return category
        return "Other"

    def _partial_matches(self, user_skills: list[str], required_skills: list[str]) -> list[dict[str, Any]]:
        partial: list[dict[str, Any]] = []
        if not user_skills or not required_skills:
            return partial
        for req in required_skills:
            if req in user_skills:
                continue
            best_skill = None
            best_score = 0.0
            for usr in user_skills:
                score = self.matcher.semantic_similarity(usr, req)
                if score > best_score:
                    best_score = score
                    best_skill = usr
            if best_skill and best_score >= 0.35:
                partial.append(
                    {
                        "required_skill": req,
                        "related_user_skill": best_skill,
                        "similarity": round(float(best_score * 100), 1),
                    }
                )
        return partial

    def _experience_level(self, user_map: dict[str, str]) -> str:
        if not user_map:
            return "Beginner"
        avg = sum(LEVEL_SCORE[v] for v in user_map.values()) / len(user_map)
        if avg >= 2.5:
            return "Advanced"
        if avg >= 1.7:
            return "Intermediate"
        return "Beginner"

    def analyze(self, user_profile: dict[str, Any], required_profile: dict[str, Any]) -> dict[str, Any]:
        user_map = self._to_map(user_profile)
        required_map = self._to_map(required_profile)

        required_skills = list(required_map.keys())
        user_skills = list(user_map.keys())
        missing: list[str] = []
        weak: list[str] = []
        matched: list[str] = []

        for skill, required_level in required_map.items():
            user_level = user_map.get(skill)
            if not user_level:
                missing.append(skill)
                continue
            matched.append(skill)
            if LEVEL_SCORE[user_level] < LEVEL_SCORE[required_level]:
                weak.append(skill)

        partial = self._partial_matches(user_skills, required_skills)
        semantic_overlap = self.matcher.semantic_overlap(user_skills, required_skills)
        exact_ratio = len(matched) / max(1, len(required_skills))
        partial_ratio = len(partial) / max(1, len(required_skills))
        weak_penalty = len(weak) / max(1, len(required_skills))

        resume_score = int(
            np.clip((exact_ratio * 70 + partial_ratio * 20 + (1 - weak_penalty) * 10), 0, 100)
        )

        category_breakdown: dict[str, int] = {}
        for category, skills in SKILL_CATEGORIES.items():
            req_count = len([s for s in required_skills if s in skills])
            have_count = len([s for s in user_skills if s in skills])
            if req_count:
                category_breakdown[category] = int(round((have_count / req_count) * 100))

        skill_gap = sorted(set(missing + weak))
        similarity = float(np.clip(self.matcher.skill_list_similarity(user_skills, required_skills), 0.0, 1.0)) * 100

        # ATS proxy: keyword coverage + category spread + weak-skill penalty.
        category_coverage = len([v for v in category_breakdown.values() if v > 0]) / max(1, len(SKILL_CATEGORIES))
        ats_score = int(np.clip(exact_ratio * 75 + category_coverage * 20 + (1 - weak_penalty) * 5, 0, 100))

        # Confidence reflects input richness + match consistency.
        confidence_score = int(
            np.clip(
                (len(required_skills) >= 4) * 20
                + (len(user_skills) >= 4) * 20
                + exact_ratio * 40
                + partial_ratio * 20,
                0,
                100,
            )
        )

        required_or_matched = sorted(set(required_skills + user_skills))
        skill_strength: dict[str, int] = {}
        for skill in required_or_matched:
            base = 30
            if skill in user_map:
                base += LEVEL_SCORE[user_map[skill]] * 20
            if skill in required_map:
                base += 10
            # Penalize if required level is above user's demonstrated level.
            if skill in required_map and skill in user_map:
                diff = LEVEL_SCORE[required_map[skill]] - LEVEL_SCORE[user_map[skill]]
                if diff > 0:
                    base -= diff * 10
            skill_strength[skill] = int(np.clip(base, 0, 100))

        top_strengths = sorted(skill_strength.items(), key=lambda kv: kv[1], reverse=True)[:3]
        risk_areas = skill_gap[:3]
        fit = "Strong" if resume_score >= 80 else "Moderate" if resume_score >= 60 else "Low"
        score_explanation = (
            f"Resume score combines exact match ({len(matched)}/{max(1, len(required_skills))}), semantic partial "
            f"matches ({len(partial)}), and level penalties ({len(weak)} under-leveled skills)."
        )
        top_partial = sorted(partial, key=lambda x: x["similarity"], reverse=True)[:2]
        partial_line = (
            "; ".join(
                [f"{p['required_skill']} ~ {p['related_user_skill']} ({p['similarity']}%)" for p in top_partial]
            )
            if top_partial
            else "No strong semantic partials detected."
        )
        strengths_line = (
            ", ".join([f"{k} ({v}%)" for k, v in top_strengths])
            if top_strengths
            else "Not enough evidence"
        )
        category_signal = ", ".join([f"{k}:{v}%" for k, v in category_breakdown.items()]) or "No category signal"
        role_fit_line = (
            "Candidate is suitable for entry-level AI Engineer scope, with upskilling needed for production ownership."
            if fit == "Moderate"
            else (
                "Candidate is strongly aligned for the role and can improve competitiveness through impact storytelling."
                if fit == "Strong"
                else "Candidate currently fits exploratory/intern-level scope and needs targeted skill closure."
            )
        )
        reasoning_trace = "\n".join(
            [
                "✔ Skill Match Insight:",
                f"- Direct alignment: {len(matched)}/{max(1, len(required_skills))} required skills matched ({', '.join(matched[:4]) or 'none'}).",
                f"- Semantic alignment: {partial_line}",
                "- Industry-readiness flag: Deployment/cloud evidence is limited."
                if "AWS" in missing or "Docker" in missing
                else "- Industry-readiness flag: Baseline deployment signals found, but depth can improve.",
                "",
                "📊 Score Breakdown:",
                f"- Resume Score ({resume_score}): Weighted by exact matches, semantic partial coverage, and level-gap penalties.",
                f"- Similarity Score ({int(round(similarity))}%): Embedding-level closeness between resume and JD skill graph.",
                f"- ATS Score ({ats_score}%): Keyword coverage + category spread + role-critical skill presence.",
                f"- Confidence Score ({confidence_score}%): Signal consistency and evidence density in extracted profile.",
                f"- Evidence snapshot: {category_signal}.",
                "",
                "💪 Key Strengths:",
                f"- Top strengths: {strengths_line}.",
                "- Core technical baseline is stable across programming, data reasoning, and backend implementation.",
                "- Demonstrates transfer potential into adjacent role requirements via semantic overlap.",
                "",
                "⚠ Critical Gaps:",
                f"- Skill risks: {', '.join(risk_areas) if risk_areas else 'No hard missing skills; primary risk is depth and production proof.'}.",
                "- Production maturity gap: limited explicit cloud/deployment ownership evidence.",
                "- Impact communication gap: add measurable outcomes (accuracy, latency, cost, uptime, business lift).",
                "",
                "🎯 Role Fit:",
                f"- {role_fit_line}",
                f"- Fit rationale: exact match={len(matched)}, partial match={len(partial)}, weak skills={len(weak)}, similarity={int(round(similarity))}%.",
                "",
                "🚀 Recommended Actions:",
                "- Build one production-style end-to-end system (data/training -> API -> deployment -> monitoring).",
                "- Add cloud execution depth with Docker + AWS/GCP deployment playbook and CI/CD.",
                "- Publish one measurable case study with before/after metrics and architecture trade-offs.",
            ]
        )

        hidden_gaps = []
        if not missing:
            if "Cloud/DevOps" in SKILL_CATEGORIES:
                devops_skills = SKILL_CATEGORIES["Cloud/DevOps"]
                if not any(s in user_skills for s in devops_skills):
                    hidden_gaps.append("Limited Cloud/DevOps exposure")
            if "Tools/Frameworks" in SKILL_CATEGORIES:
                tf_skills = SKILL_CATEGORIES["Tools/Frameworks"]
                if len([s for s in user_skills if s in tf_skills]) < 2:
                    hidden_gaps.append("Shallow tools/framework depth")
            hidden_gaps.append("Need more real-world impact evidence (scale, reliability, ownership)")

        skill_categories = {
            category: sorted([s for s in required_or_matched if s in skills])
            for category, skills in SKILL_CATEGORIES.items()
        }
        return {
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
            "partial_matches": partial,
            "weak_skills": sorted(weak),
            "skill_gap": skill_gap,
            "scores": {
                "resume_score": resume_score,
                "similarity_score": int(round(similarity)),
                "ats_score": ats_score,
                "confidence_score": confidence_score,
                "score_explanation": score_explanation,
            },
            "experience_level": self._experience_level(user_map),
            "skill_strength": skill_strength,
            "skill_gap_analysis": (
                "No direct missing skills. Hidden gaps: " + "; ".join(hidden_gaps)
                if not missing
                else "Missing or under-leveled skills require focused progression before advanced specialization."
            ),
            "reasoning_trace": reasoning_trace,
            "skill_categories": skill_categories,
            "user_skills": user_skills,
            "required_skills": required_skills,
            "skill_breakdown": category_breakdown,
        }
