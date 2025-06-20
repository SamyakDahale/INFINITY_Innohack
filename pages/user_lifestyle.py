import streamlit as st
import sidebar
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Only initialize Firebase if not already initialized
if not firebase_admin._apps:
    # Load credentials from Streamlit secrets
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# === Sidebar and Style ===
sidebar.render_sidebar()

# === Custom Theme, Layout & Animation CSS ===
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Rubik', sans-serif;
            background: linear-gradient(to right, #f8c6ff, #dab7f7);
            color: #4b0082;
        }

        .block-container {
            background-color: rgba(255, 255, 255, 0.96);
            border-radius: 1.5rem;
            padding: 2rem 3rem;
            margin-top: 2rem;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
            animation: fadeIn 1.2s ease-in-out;
        }

        .stSelectbox > div > div {
            border: 2px solid #d6a8ed !important;
            border-radius: 10px;
            color: #4b0082;
        }

        .stButton > button {
            background-color: #ba55d3;
            color: white;
            font-weight: 600;
            padding: 0.5rem 1.2rem;
            border-radius: 10px;
            transition: 0.3s;
            animation: slideUp 1s ease-in-out;
        }

        .stButton > button:hover {
            background-color: #9932cc;
            transform: scale(1.05);
        }

        .score-box {
            font-size: 1.5rem;
            background: #ffe6ff;
            padding: 1rem;
            margin-top: 1.5rem;
            border-left: 6px solid #ba55d3;
            border-radius: 10px;
            color: #4b0082;
            animation: fadeIn 1.5s ease-in-out;
        }

        h2, h4, .stMarkdown {
            animation: fadeIn 1.5s ease-in-out;
        }

        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }

        @keyframes slideUp {
            0% {opacity: 0; transform: translateY(20px);}
            100% {opacity: 1; transform: translateY(0);}
        }
    </style>
""", unsafe_allow_html=True)

# === Page Title ===
st.markdown('<h2 style="text-align:center;">🌱 Lifestyle Health Score Calculator</h2>', unsafe_allow_html=True)
st.markdown("#### ✨ Answer the lifestyle questions to calculate your health score")

# === Option Labels and Mapping ===
options = {
    "Never": 0,
    "Rarely": 1,
    "Occasionally": 2,
    "Frequently": 3,
    "Very Frequently": 4,
    "Always": 5
}

# === User Inputs ===
col1, col2 = st.columns(2)

with col1:
    exercise_label = st.selectbox("💪 Exercise", list(options.keys()))
    smoking_label = st.selectbox("🚬 Smoking", list(options.keys()))
    drinking_label = st.selectbox("🍺 Drinking", list(options.keys()))

with col2:
    job_hazard_label = st.selectbox("⚠ Job Hazard", list(options.keys()))
    mental_stress_label = st.selectbox("🧠 Mental Stress", list(options.keys()))

# === Calculate Score ===
if st.button("🎯 Calculate Health Score"):
    # Convert to numeric
    exercise = options[exercise_label]
    smoking = options[smoking_label]
    drinking = options[drinking_label]
    job_hazard = options[job_hazard_label]
    mental_stress = options[mental_stress_label]

    # Fetch company lifestyle data
    docs = db.collection("company_lifestyle").stream()

    total_docs = 0
    sum_weights = {k: 0 for k in ["exercise", "smoking", "drinking", "job_hazard", "mental_stress"]}

    for doc in docs:
        data = doc.to_dict()
        total_docs += 1
        for key in sum_weights:
            sum_weights[key] += data.get(key, 0)

    if total_docs == 0:
        st.error("⚠ No company lifestyle data available.")
        st.stop()

    # Normalize weights
    avg_weights = {k: v / total_docs for k, v in sum_weights.items()}
    total_weight = sum(avg_weights.values())
    normalized_weights = {k: v / total_weight for k, v in avg_weights.items()}

    adjusted_exercise = 5 - exercise  # reverse for positive effect

    weighted_sum = (
        adjusted_exercise * normalized_weights["exercise"] +
        smoking * normalized_weights["smoking"] +
        drinking * normalized_weights["drinking"] +
        job_hazard * normalized_weights["job_hazard"] +
        mental_stress * normalized_weights["mental_stress"]
    )

    health_score = max(0, min(5, weighted_sum))

    st.markdown(f"""
        <div class="score-box">
            💖 Your calculated health score is: <strong>{health_score:.2f} / 5</strong>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.health_score = health_score