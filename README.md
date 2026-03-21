# AI Adaptive Onboarding Engine

End-to-end AI onboarding system that analyzes a candidate resume against a job description, detects skill gaps, and produces a personalized learning roadmap with explainable reasoning.

## Features
- Resume parsing (TXT/PDF) and JD parsing
- Skill extraction with synonym normalization
- Skill level detection (beginner/intermediate/advanced)
- Skill gap analysis + resume score
- Semantic matching using sentence-transformers (`all-MiniLM-L6-v2`)
- Adaptive roadmap generation with dependency-aware ordering
- No-gap advanced learning path fallback (roadmap always generated)
- Professional React dashboard with:
  - Upload feedback (`Upload successful`, `Processing`, `Analysis complete`)
  - Resume score cards
  - Pie chart for skill category coverage
  - Progress bars
  - Recommendations section
  - Reasoning trace section

## Folder Structure
```
AI-Onboarding-Engine/
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── services/
│   └── utils/
├── frontend/
│   ├── src/
│   └── package.json
├── models/
├── docs/
├── Dockerfile
├── requirements.txt
└── README.md
```

## Architecture Diagram (Text)
```
[React Frontend]
    -> upload resume/JD
    -> trigger /analyze
[FastAPI Backend]
    -> parse text
    -> extract skills + levels
    -> run semantic + gap analysis
    -> generate adaptive roadmap
    -> return reasoning JSON
[Dashboard]
    -> render score, gap, chart, roadmap, recommendations
```

## Setup

### Backend
```bash
cd AI-Onboarding-Engine
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

### Optional spaCy setup
spaCy is optional in this project. If you want spaCy model-based extensions:

- Use Python `3.11` or `3.12` (recommended for spaCy compatibility)
- Then run:

```bash
pip install -r requirements-spacy.txt
python -m spacy download en_core_web_sm
```

If you are on Python `3.14`, skip spaCy install/download steps.

### Frontend
```bash
cd AI-Onboarding-Engine/frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` and backend on `http://localhost:8000`.

## API Endpoints
- `POST /upload-resume` - Upload resume file
- `POST /upload-jd` - Upload job description file
- `POST /analyze` - Execute extraction, matching, scoring, and roadmap generation
- `GET /roadmap` - Return latest roadmap
- `GET /health` - Health check

## Response Format
```json
{
  "scores": {
    "resume_score": 0,
    "similarity_score": 0,
    "ats_score": 0,
    "confidence_score": 0
  },
  "skills": {
    "matched": [],
    "missing": [],
    "partial": []
  },
  "experience_level": "",
  "skill_strength": {},
  "skill_gap_analysis": "",
  "learning_roadmap": [],
  "reasoning_trace": ""
}
```

## Models Used
- **Skill extraction:** rule-based NLP with taxonomy + synonyms (extensible to spaCy/LLM)
- **Similarity model:** sentence-transformers `all-MiniLM-L6-v2`
- **Adaptive logic:** dependency-aware graph ordering + advanced fallback path

## Dataset References
- `models/learning_dataset.json` (dummy curated learning resources)
- Sample testing files:
  - `docs/sample_resume.txt`
  - `docs/sample_jd.txt`

## Docker
```bash
cd AI-Onboarding-Engine
docker build -t ai-onboarding-engine .
docker run -p 8000:8000 ai-onboarding-engine
```

## Bonus Upgrade Hooks
- Add OpenAI/Gemini reasoning enhancer in `learning_path_generator.py`
- Persist sessions and user auth using SQLite/PostgreSQL + JWT
- Add radar chart and timeline roadmap views
