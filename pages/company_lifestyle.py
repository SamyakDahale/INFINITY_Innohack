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


# Streamlit Page Config
st.set_page_config(
    page_title="Lifestyle Factors",
    layout="wide",
)

sidebar.render_sidebar()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("companystyle.css")

# ---------- Page Heading ----------
st.markdown("## 🧬 Lifestyle Factors")
st.markdown("Set the percentage impact of lifestyle factors on insurance premiums")

# ---------- Input Form ----------
with st.form("lifestyle_form"):
    exercise = st.number_input("Exercise (%)", min_value=0, max_value=100, step=1, key="ex")
    smoking = st.number_input("Smoking (%)", min_value=0, max_value=100, step=1, key="sm")
    drinking = st.number_input("Drinking (%)", min_value=0, max_value=100, step=1, key="dr")
    job_hazard = st.number_input("Job Hazard (%)", min_value=0, max_value=100, step=1, key="jh")
    mental_stress = st.number_input("Mental Stress (%)", min_value=0, max_value=100, step=1, key="ms")

    total = exercise + smoking + drinking + job_hazard + mental_stress
    st.markdown(f"**Total: {total}%**")

    submitted = st.form_submit_button("💾 Save Lifestyle Factors")

# ---------- Submission Logic ----------
if submitted:
    if total != 100:
        st.warning("⚠️ Total must be exactly 100% to submit.")
    else:
        if "username" not in st.session_state or st.session_state.get("user_type") != "Company":
            st.error("⚠️ Please log in as a company to update lifestyle factors.")
            st.stop()

        company_username = st.session_state.username

        lifestyle_data = {
            "company_name": company_username,
            "exercise": exercise,
            "smoking": smoking,
            "drinking": drinking,
            "job_hazard": job_hazard,
            "mental_stress": mental_stress
        }

        # Create or update Firestore document
        db.collection("company_lifestyle").document(company_username).set(lifestyle_data)

        st.success("✅ Lifestyle factors updated successfully!")
