class MatchingModel:
    def __init__(self) -> None:
        self.related = {
            "AWS": ["Cloud/DevOps", "Docker", "Kubernetes", "GCP", "Azure"],
            "Machine Learning": ["Data Analysis", "NLP", "Deep Learning"],
            "Data Analysis": ["Machine Learning", "SQL", "Python"],
            "FastAPI": ["Backend Development", "Python", "Django"],
            "React": ["JavaScript", "Frontend Development"],
            "SQL": ["Data Analysis", "PostgreSQL"],
            "Kubernetes": ["Docker", "Cloud/DevOps"],
        }

    def _simple_similarity(self, a: str, b: str) -> float:
        aset = set(a.lower().split())
        bset = set(b.lower().split())
        if not aset or not bset:
            return 0.0
        return len(aset & bset) / len(aset | bset)

    def skill_list_similarity(self, user_skills: list[str], required_skills: list[str]) -> float:
        if not user_skills or not required_skills:
            return 0.0
        return sum(self._simple_similarity(x, y) for x in user_skills for y in required_skills) / (
            len(user_skills) * len(required_skills)
        )

    def semantic_similarity(self, a: str, b: str) -> float:
        if a.lower() == b.lower():
            return 1.0
        related_a = set(self.related.get(a, []))
        related_b = set(self.related.get(b, []))
        if b in related_a or a in related_b or related_a & related_b:
            return 0.62
        return self._simple_similarity(a, b)

    def semantic_overlap(self, user_skills: list[str], required_skills: list[str], threshold: float = 0.6) -> int:
        if not user_skills or not required_skills:
            return 0
        return sum(
            1 for req in required_skills
            if max(self.semantic_similarity(req, usr) for usr in user_skills) >= threshold
        )
