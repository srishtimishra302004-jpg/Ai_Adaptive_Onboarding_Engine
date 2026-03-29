from models.matching_model import MatchingModel
from models.skill_taxonomy import SKILL_CATEGORIES

LEVEL_SCORE = {"beginner": 1, "intermediate": 2, "advanced": 3}


class GapAnalyzer:
    def __init__(self) -> None:
        self.matcher = MatchingModel()

    def _to_map(self, profile: dict) -> dict:
        return {item["skill"]: item["level"] for item in profile.get("skills", [])}

    def _partial_matches(self, user_skills: list, required_skills: list) -> list:
        partial = []
        for req in required_skills:
            if req in user_skills:
                continue
            best_skill, best_score = None, 0.0
            for usr in user_skills:
                score = self.matcher.semantic_similarity(usr, req)
                if score > best_score:
                    best_score, best_skill = score, usr
            if best_skill and best_score >= 0.35:
                partial.append({
                    "required_skill": req,
                    "related_user_skill": best_skill,
                    "similarity": round(best_score * 100, 1),
                })
        return partial

    def _experience_level(self, user_map: dict) -> str:
        if not user_map:
            return "Beginner"
        avg = sum(LEVEL_SCORE[v] for v in user_map.values()) / len(user_map)
        if avg >= 2.5:
            return "Advanced"
        if avg >= 1.7:
            return "Intermediate"
        return "Beginner"

    def analyze(self, user_profile: dict, required_profile: dict) -> dict:
        user_map = self._to_map(user_profile)
        required_map = self._to_map(required_profile)
        required_skills = list(required_map.keys())
        user_skills = list(user_map.keys())

        matched, missing, weak = [], [], []
        for skill, req_level in required_map.items():
            user_level = user_map.get(skill)
            if not user_level:
                missing.append(skill)
            else:
                matched.append(skill)
                if LEVEL_SCORE[user_level] < LEVEL_SCORE[req_level]:
                    weak.append(skill)

        partial = self._partial_matches(user_skills, required_skills)
        exact_ratio = len(matched) / max(1, len(required_skills))
        partial_ratio = len(partial) / max(1, len(required_skills))
        weak_penalty = len(weak) / max(1, len(required_skills))

        resume_score = int(min(100, max(0, exact_ratio * 70 + partial_ratio * 20 + (1 - weak_penalty) * 10)))
        similarity = min(1.0, max(0.0, self.matcher.skill_list_similarity(user_skills, required_skills))) * 100

        category_breakdown = {
            cat: int(round(len([s for s in user_skills if s in skills]) / max(1, len([s for s in required_skills if s in skills])) * 100))
            for cat, skills in SKILL_CATEGORIES.items()
            if any(s in required_skills for s in skills)
        }
        category_coverage = len([v for v in category_breakdown.values() if v > 0]) / max(1, len(SKILL_CATEGORIES))
        ats_score = int(min(100, max(0, exact_ratio * 75 + category_coverage * 20 + (1 - weak_penalty) * 5)))
        confidence_score = int(min(100, max(0,
            (len(required_skills) >= 4) * 20 + (len(user_skills) >= 4) * 20 +
            exact_ratio * 40 + partial_ratio * 20
        )))

        all_skills = sorted(set(required_skills + user_skills))
        skill_strength = {}
        for skill in all_skills:
            base = 30
            if skill in user_map:
                base += LEVEL_SCORE[user_map[skill]] * 20
            if skill in required_map:
                base += 10
                if skill in user_map:
                    diff = LEVEL_SCORE[required_map[skill]] - LEVEL_SCORE[user_map[skill]]
                    if diff > 0:
                        base -= diff * 10
            skill_strength[skill] = int(min(100, max(0, base)))

        skill_gap = sorted(set(missing + weak))
        fit = "Strong" if resume_score >= 80 else "Moderate" if resume_score >= 60 else "Low"
        top_strengths = sorted(skill_strength.items(), key=lambda kv: kv[1], reverse=True)[:3]

        reasoning_trace = "\n".join([
            f"✔ Matched {len(matched)}/{max(1, len(required_skills))} required skills.",
            f"📊 Resume: {resume_score} | Similarity: {int(round(similarity))}% | ATS: {ats_score}% | Confidence: {confidence_score}%",
            f"💪 Top strengths: {', '.join(f'{k} ({v}%)' for k, v in top_strengths) or 'N/A'}",
            f"⚠ Gaps: {', '.join(skill_gap[:3]) or 'None'}",
            f"🎯 Fit: {fit}",
        ])

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
            },
            "experience_level": self._experience_level(user_map),
            "skill_strength": skill_strength,
            "skill_gap_analysis": (
                "Missing or under-leveled skills require focused progression before advanced specialization."
                if missing else "No direct missing skills. Focus on depth and production outcomes."
            ),
            "reasoning_trace": reasoning_trace,
            "skill_categories": {
                cat: sorted([s for s in all_skills if s in skills])
                for cat, skills in SKILL_CATEGORIES.items()
            },
            "user_skills": user_skills,
            "required_skills": required_skills,
            "skill_breakdown": category_breakdown,
        }
