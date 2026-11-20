"""Static profile facts shown in the UI (About page, timeline, KPIs).
Source: Vrushank_Dhande_Resume.pdf (2026). Update here when the resume changes;
the chatbot's answers come from MongoDB, not from this file."""

PROFILE = {
    "name": "Vrushank Dhande",
    "title": "AI/ML Engineer",
    "location": "Pune, India",
    "experience": "5+",
    "summary": (
        "Artificial Intelligence Engineer with 5+ years of experience designing, developing, and "
        "deploying end-to-end AI/ML solutions and scalable software applications across finance, "
        "media, and industrial domains."
    ),
    "links": {
        "Portfolio": "https://vrushankdhande.github.io/",
        "GitHub": "https://github.com/vrushankdhande",
        "LinkedIn": "https://www.linkedin.com/in/vrushankdhande/",
        "Kaggle": "https://www.kaggle.com/vrushankdhande",
        "Medium": "https://medium.com/@vrushankdhande",
    },
}

# end=None means current role
ROLES = [
    {"company": "ERGOBITE Tech Solutions", "role": "AI/ML Engineer", "start": "2026-04-01", "end": None,
     "period": "Apr 2026 – Present", "location": "Pune",
     "highlights": [
         "Dynamic model-switching logic that cut token usage and operational costs by 76%.",
         "Wealth-management app with LLM reasoning, deployed on Kubernetes in 2 weeks.",
         "AI invoice-extraction finance portal that cut manual processing time by 97%.",
         "AI voice agent that handled 67+ client calls independently.",
         "Corporate Travel Booking Portal (TripJack APIs, Razorpay, wallet management).",
         "Claude token calculator and usage-tracking platform with admin dashboard.",
     ]},
    {"company": "SAREGAMA India", "role": "Business Analyst in AI", "start": "2023-09-01", "end": "2026-04-01",
     "period": "Sep 2023 – Apr 2026", "location": "Mumbai",
     "highlights": [
         "Automated reporting pipeline (Python, SQL, APIs) that reduced extraction errors by 20%.",
         "YOLOv3 + FAISS copyright-violation detection: tripled accuracy, backlog down 40%.",
         "Company's first unified ticketing data-extraction pipeline with RAG-based insights.",
         "Song-mapping engine with Prophet + LSTM revenue forecasts (+20% accuracy).",
         "Real-time song-event monitoring that saved 200+ operational hours.",
     ]},
    {"company": "EATON India", "role": "Data Science Intern", "start": "2022-06-01", "end": "2022-07-31",
     "period": "Jun 2022 – Jul 2022", "location": "Pune",
     "highlights": [
         "YOLOv3/v5 defect detection that reduced manual inspection effort by 70%.",
         "Knowledge distillation: model size down 45%, inference 30% faster, >95% accuracy.",
     ]},
    {"company": "Groom", "role": "Machine Learning Intern", "start": "2021-09-01", "end": "2022-05-31",
     "period": "Sep 2021 – May 2022", "location": "Mumbai",
     "highlights": [
         "Augmentation pipelines that boosted validation accuracy by 15–20%.",
         "Multi-class image classifiers at 89% accuracy (OpenCV, TensorFlow).",
     ]},
]

SKILLS = {
    "GenAI / LLM": ["RAG", "LangChain", "LangGraph", "Prompt Engineering", "Transformers", "Agentic AI"],
    "Deep Learning": ["CNN", "RNN", "YOLOv3–v5", "Transfer Learning", "Time-Series Forecasting"],
    "Machine Learning": ["Supervised & Unsupervised", "Model Interpretability", "Feature Selection"],
    "Languages": ["Python", "SQL", "R"],
    "Platforms": ["Docker", "Kubernetes", "Azure", "FastAPI", "Flask", "Streamlit", "MySQL", "Tableau"],
}

EDUCATION = [
    ("B.E. Electronics Engineering — VESIT, Mumbai", "2019–2023 · CGPA 8.54"),
    ("HSC — K.T.H.M College, Nashik", "2017–2019 · 68.23%"),
    ("SSC — Rangubai Junnare High School, Nashik", "2017 · 82.60%"),
]

SPOKEN_LANGUAGES = ["English (Native)", "German (Fluent)", "French (Conversational)"]
