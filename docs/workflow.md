# Workflow

1. User uploads `resume.pdf/txt` and `jd.pdf/txt` from frontend.
2. Backend extracts text via file handler (supports PDF via PyMuPDF fallback).
3. NLP layer normalizes text and maps synonyms (e.g., `ML` -> `Machine Learning`).
4. Skill extractor identifies skills and inferred levels (`beginner/intermediate/advanced`).
5. Gap analyzer compares resume profile with JD profile:
   - exact overlap
   - semantic overlap (sentence-transformers)
   - score computation
6. Learning path generator:
   - if gap exists -> dependency-aware gap-closure path
   - if no gap -> advanced growth path (always returns roadmap)
7. Dashboard visualizes all outputs + reasoning trace.
