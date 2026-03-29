# Architecture

## System Components
- **Frontend (React + Vite):** Uploads resume and JD, triggers analysis, visualizes scores/gaps/roadmap.
- **Backend (FastAPI):** Handles parsing, extraction, gap analysis, adaptive planning, and reasoning trace output.
- **Models Layer:** Skill taxonomy, semantic similarity model (`all-MiniLM-L6-v2`), and adaptive dependency algorithm.
- **Dataset:** `models/learning_dataset.json` maps skills + levels to curated learning resources.

## Text Architecture Diagram
[User]
  -> [React Upload Page]
  -> POST /upload-resume, /upload-jd
  -> POST /analyze
      -> ResumeParser + JDParser
      -> SkillExtractor (synonyms + level inference)
      -> GapAnalyzer (exact + semantic matching + score)
      -> AdaptiveRoadmapEngine (dependency-aware ordering)
  <- JSON response (skills, gaps, roadmap, reasoning, score)
  -> [React Dashboard Page]
## Scalability Notes
- Parser and model services are stateless and can be horizontally scaled.
- In-memory state can be swapped for SQLite or Redis for multi-user support.
- Skill extraction can be upgraded to external LLM provider with minimal route changes.
