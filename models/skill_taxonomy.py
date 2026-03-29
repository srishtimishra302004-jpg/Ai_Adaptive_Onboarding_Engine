SKILL_SYNONYMS = {
    "ml": "Machine Learning",
    "py": "Python",
    "js": "JavaScript",
    "ts": "TypeScript",
    "postgres": "PostgreSQL",
    "reactjs": "React",
    "k8s": "Kubernetes",
    "ci/cd": "CI/CD",
    "nlp": "NLP",
    "llm": "NLP",
    "hr analytics": "People Analytics",
    "talent acquisition": "Recruitment",
    "salesforce": "CRM",
    "finite element analysis": "FEA",
    "cad/cam": "CAD",
}

SKILL_CATEGORIES = {
    "Programming": ["Python", "JavaScript", "TypeScript", "SQL"],
    "Data/AI": [
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Data Analysis",
        "TensorFlow",
        "PyTorch",
        "People Analytics",
        "Sales Forecasting",
        "Predictive Maintenance",
    ],
    "Tools/Frameworks": [
        "FastAPI",
        "React",
        "Django",
        "Git",
        "PostgreSQL",
        "Docker",
        "CRM",
        "ATS",
        "CAD",
        "FEA",
        "Recruitment",
    ],
    "Cloud/DevOps": ["AWS", "Azure", "GCP", "Kubernetes", "CI/CD"],
}

ALL_SKILLS = sorted({item for values in SKILL_CATEGORIES.values() for item in values})
