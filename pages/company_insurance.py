import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json



# Only initialize Firebase if not already initialized
if not firebase_admin._apps:
    # Load credentials from Streamlit secrets
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

import sidebar


st.set_page_config(
    page_title="Add Insurance Plan",
    layout="wide",
)

sidebar.render_sidebar()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("companystyle.css")

# ---------- Top Navigation ----------
st.markdown('<div class="top-bar">Insurance Admin Dashboard</div>', unsafe_allow_html=True)
st.markdown("📄 Add New Insurance Plan")

# ---------- Form Layout ----------
with st.form("insurance_form"):
    col1, col2 = st.columns(2)

    with col1:
        insurance_name = st.text_input("Insurance Plan Name")
        ExistingDiagnosis = st.selectbox(
                "Pre-existing diseases covered",
                ["None", "Ashtma", "Cancer", "HIV", "Tubercolosis", "Parkinsons"]
            )
        Med_Condition = st.selectbox(
                "Medical Condition covered",
                ["Fit", "Diabetes", "Hypertension", "Anemia", "High_Cholestrol"]
            )
        premium = st.number_input("Premium (per 10L of SA (in ₹))", min_value=0)
        premium_type = st.radio("Premium Type", ["Constant", "Floating"])

    with col2:
        addons = st.multiselect(
            "Select Add-ons",
            [
                "Critical Illness Cover",  "Maternity Cover", "Room Rent Waiver",  "Hospital Cash Benefit",
                "OPD Cover", "Accidental Death & Disability Cover", "International Coverage",
            ]
        )
        health_score = st.slider(" Minimum Health Score required", 0.0, 5.0, 2.0, 0.1)
        description = st.text_area("Description")

    submitted = st.form_submit_button("➕ Add Insurance Plan")
    if submitted:
        if "username" not in st.session_state:
            st.error("⚠️ Company name not found in session. Please log in again.")
        else:
            # Structure the data
            insurance_data = {
                "insurance_name": insurance_name,
                "existing_diagnosis": ExistingDiagnosis,
                "medical_condition": Med_Condition,
                "premium": premium,
                "premium_type": premium_type,
                "addons": addons,
                "min_health_score": health_score,
                "description": description,
                "company_name": st.session_state["username"]
            }


            try:
                db.collection("INSURANCE_PLANS").add(insurance_data)
                st.success("✅ Insurance Plan added successfully!")
            except Exception as e:
                st.error(f"❌ Failed to add plan: {e}")

      