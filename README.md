# AI Adaptive Onboarding Engine

End-to-end AI onboarding system that analyzes a candidate resume against a job description, detects skill gaps, and produces a personalized learning roadmap with explainable reasoning.
The goal is simple:  
1.) Reduce unnecessary training  
2.) Focus only on what the candidate actually needs  

## What This Project Does
Instead of giving every new hire the same training, this system:
- Understands what the candidate already knows  
- Compares it with job requirements  
- Identifies missing or weak areas
- Generates a structured learning path  
- Explains *why* those recommendations were mad

## Key Features
-  Resume & Job Description parsing (TXT/PDF)
-  Skill extraction with synonym handling
-  Resume scoring + similarity analysis
-  Semantic matching using `sentence-transformers`
-  Skill gap detection (including hidden gaps)
-  Adaptive learning roadmap generation
-  Explainable reasoning trace 
-  Interactive dashboard with:
  - Score cards
  - Skill breakdown charts
  - Progress indicators
  - Recommendations
  - Reasoning insights

## Folder Structure
AI-Onboarding-Engine/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── requirements-spacy.txt
│   ├── routes.py
│   ├── services/
│   └── utils/
├── frontend/
│   ├── src/
│   └── package.json
├── models/
├── docs/
├── Dockerfile
└── README.md

## Render Deployment Notes

### Backend service (Render Web Service)
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Frontend service (Render Static Site)
- Root Directory: `frontend`
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`
## Tech Stack
**Frontend**
- React (Vite)
- Chart.js (for visualization)
- 
**Backend**
- FastAPI
- Python
- 
**AI / NLP**
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Rule-based skill extraction + normalization

## Architecture Diagram 
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
    
## Setup
### Backend
```bash
cd AI-Onboarding-Engine/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```
### Frontend
```bash
[dashboard](https://ai-onboarding-engine.vercel.app/)
cd AI-Onboarding-Engine/frontend
npm install
npm run dev

Frontend runs on: 'http://localhost:5173'


