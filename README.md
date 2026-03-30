# AI Adaptive Onboarding Engine
End-to-end AI onboarding system that analyzes a candidate resume against a job description and understand their current skils, detects skill gaps, and produces a personalized learning roadmap with explainable reasoning for improvement.

The goal is to:  
1.) Reduce unnecessary training  
2.) Focus only on what the candidate actually needs  

## What This Project Does
Instead of giving every new hire the same training, this system:
- Understands what the candidate already knows  
- Compares it with job requirements  
- Identifies missing or weak areas
- Generates a structured learning path  
- Explains *why* those recommendations were made

## Team Contribution
This project was developed as a collaborative team effort. Each team member contributed to different aspects of the system:
- Designing AI-based logic for skill gap analysis
- Developing backend APIs and services
- Building interactive frontend UI
- Integrating frontend with backend
- Testing and debugging the application
This project highlights teamwork, problem-solving, and real-world AI application development.

## Key Features
-  Resume & Job Description parsing (TXT/PDF)
-  Skill extraction with synonym handling
-  Resume scoring + similarity analysis
-  Skill gap detection (including hidden gaps)
-  Adaptive learning roadmap generation
-  Explainable reasoning trace 
-  Interactive dashboard with:
   - Skill breakdown charts
   - Progress indicators
   - Recommendations
   - Reasoning insights

## Folder Structure
```
AI_ADAPTIVE_ENGINE/
│
├── backend/
│   ├── services/
│   │   ├── gap_analyzer.py
│   │   ├── skill_extractor.py
│   ├── utils/
│   ├── app.py
│   ├── routes.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── styles.css
│   ├── index.html
│
├── models/
│   ├── adaptive_algorithm.py
│   ├── skill_taxonomy.py
│   ├── learning_dataset.json
│
├── requirements.txt
├── README.md
├── railway.toml
 ```

## Tech Stack
**Frontend**
- React (Vite)
- Chart.js (for visualization)
  
**Backend**
- FastAPI
- Python
 
**AI / NLP**
- Rule-based skill extraction + normalization

## Architecture Diagram 
```
[React Frontend]
    -> upload resume/JD
    -> trigger /analyze
```
```
[FastAPI Backend]
    -> parse text
    -> extract skills + levels
    -> run semantic + gap analysis
    -> generate adaptive roadmap
    -> return reasoning JSON
```
```
[Dashboard]
    -> score, gap, chart, roadmap, recommendations, reasoning trace
```
    
## How to Run Locally
- 1️⃣ Clone the Repository
  - git clone - https://github.com/srishtimishra302004-jpg/Ai_Adaptive_Onboarding_Engine
  - cd AI-Adaptive-Onboarding-Engine
- 2️⃣ Backend Setup
  - cd ~/Downloads/Ai_adaptive_engine
  - pip install -r requirements.txt
  - uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
  - Backend will run on:
    http://127.0.0.1:8000
- 3️⃣ Frontend Setup
  - cd ~/Downloads/Ai_adaptive_engine/frontend
  - npm install
  - npm run dev
  - Frontend will run on:
    http://localhost:5173
- 4️⃣ Optional (Virtual Environment Recommended)
  - python -m venv venv
  - venv\Scripts\activate   
  - pip install -r requirements.txt

## Deployment
 Live Project Link:
- Frontend- https://ai-adaptive-onboarding-engine-kappa.vercel.app?_vercel_share=NnIumuOUUcJkucg0uAEukEdhOO1oXnuI 
- Backend- https://aiadaptiveonboardingengine-production.up.railway.app/ 

## Future Enhancements
- Integration with LLM
- Dashboard with analytics
- User authentication system
- Mobile responsiveness improvements

## Acknowledgment
Special thanks to all team members for their collaboration and contribution in making this project successful.
### Team Members: 
- Narottam Kumar
- Siddharth Karn
- Ankit Kumar
- Srishti Mishra

