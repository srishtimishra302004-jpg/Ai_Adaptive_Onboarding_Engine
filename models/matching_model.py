from __future__ import annotations

import math
from typing import Iterable


class MatchingModel:
    def __init__(self) -> None:
        self.model = None
        self.related = {
            "AWS": ["Cloud/DevOps", "Docker", "Kubernetes", "GCP", "Azure"],
            "Machine Learning": ["Data Analysis", "NLP", "Deep Learning"],
            "Data Analysis": ["Machine Learning", "SQL", "Python"],
            "FastAPI": ["Backend Development", "Python", "Django"],
            "React": ["JavaScript", "Frontend Development"],
            "SQL": ["Data Analysis", "PostgreSQL"],
            "Kubernetes": ["Docker", "Cloud/DevOps"],
        }
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            self.model = None

    def _simple_similarity(self, a: str, b: str) -> float:
        aset = set(a.lower().split())
        bset = set(b.lower().split())
        if not aset or not bset:
            return 0.0
        return len(aset.intersection(bset)) / len(aset.union(bset))

    def _cosine(self, vec_a, vec_b) -> float:
        dot = float((vec_a * vec_b).sum())
        denom = math.sqrt(float((vec_a * vec_a).sum())) * math.sqrt(float((vec_b * vec_b).sum()))
        return dot / denom if denom else 0.0

    def skill_list_similarity(self, user_skills: Iterable[str], required_skills: Iterable[str]) -> float:
        u = list(user_skills)
        r = list(required_skills)
        if not u or not r:
            return 0.0
        if self.model is None:
            return sum(self._simple_similarity(x, y) for x in u for y in r) / (len(u) * len(r))

        u_vec = self.model.encode([" ".join(u)])[0]
        r_vec = self.model.encode([" ".join(r)])[0]
        return self._cosine(u_vec, r_vec)

    def semantic_similarity(self, a: str, b: str) -> float:
        if a.lower() == b.lower():
            return 1.0
        related_a = set(self.related.get(a, []))
        related_b = set(self.related.get(b, []))
        if b in related_a or a in related_b or related_a.intersection(related_b):
            return 0.62
        if self.model is None:
            return self._simple_similarity(a, b)
        vecs = self.model.encode([a, b])
        return float(self._cosine(vecs[0], vecs[1]))

    def semantic_overlap(self, user_skills: list[str], required_skills: list[str], threshold: float = 0.6) -> int:
        if not user_skills or not required_skills:
            return 0
        hits = 0
        for req in required_skills:
            best = max(self.semantic_similarity(req, usr) for usr in user_skills)
            if best >= threshold:
                hits += 1
        return hits
