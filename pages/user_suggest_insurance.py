import streamlit as st
import sidebar
sidebar.render_sidebar()

import firebase_admin
from firebase_admin import credentials, firestore
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import json

# Only initialize Firebase if not already initialized
if not firebase_admin._apps:
    # Load credentials from Streamlit secrets
    firebase_credentials = json.loads(json.dumps(st.secrets["firebase"]))
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# === Custom CSS for Cards ===
st.markdown("""
    <style>
        .card {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .card h3 {
            margin-top: 0;
            color: #0096c7;
        }
        .card p {
            margin: 6px 0;
        }
    </style>
""", unsafe_allow_html=True)

st.subheader("📋 Your Health Summary")

if "health_score" in st.session_state and "medical_conditions" in st.session_state and "existing_diagnosis" in st.session_state:
    health_score = st.session_state.health_score
    medical_conditions = st.session_state.medical_conditions
    existing_diagnosis = st.session_state.existing_diagnosis

    st.markdown(f"- *Health Score*: {health_score}")
    st.markdown(f"- *Medical Conditions*: {medical_conditions}")
    st.markdown(f"- *Existing Diagnoses*: {existing_diagnosis}")

    user_premium = st.number_input("Expected Premium", min_value=0)
    user_premium_type = st.radio("Premium Type wanted", ["Constant", "Floating"])
    user_addons = st.multiselect(
        "Select Add-ons",
        [
            "Critical Illness Cover", "Maternity Cover", "Room Rent Waiver", "Hospital Cash Benefit",
            "OPD Cover", "Accidental Death & Disability Cover", "International Coverage",
        ]
    )
else:
    st.warning("Health data not found in session.")
    st.stop()

# === Suggest Plan Button ===
if "show_results" not in st.session_state:
    st.session_state.show_results = False

if st.button("🎯 Suggest Suitable Plans"):
    st.session_state.show_results = True

if st.session_state.show_results:
    plans_ref = db.collection("INSURANCE_PLANS").stream()

    plans = []
    similarities = []
    for doc in plans_ref:
        plan = doc.to_dict()
        plan_name = plan.get("insurance_name", "Unnamed Plan")

        plan_health = plan.get("min_health_score", 0)
        plan_conditions = plan.get("medical_condition", [])
        plan_diagnosis = plan.get("existing_diagnosis", [])
        plan_premium = plan.get("premium", 0)
        plan_addons = plan.get("addons", [])
        plan_premium_type = plan.get("premium_type", "")

        match_health = 1 if health_score >= plan_health else 0
        match_condition = 1 if any(cond in medical_conditions for cond in plan_conditions) else 0
        match_diagnosis = 1 if any(diag in existing_diagnosis for diag in plan_diagnosis) else 0
        match_premium = 1 if plan_premium <= user_premium else 0
        match_premium_type = 1 if plan_premium_type == user_premium_type else 0
        match_addon = 1 if any(add in plan_addons for add in user_addons) else 0

        user_vector = np.array([1, 1, 1, 1, 1, 1])
        plan_vector = np.array([
            match_health,
            match_condition,
            match_diagnosis,
            match_premium,
            match_premium_type,
            match_addon
        ])

        similarity = cosine_similarity([user_vector], [plan_vector])[0][0]
        similarities.append((similarity, plan_name, plan))

    similarities.sort(reverse=True, key=lambda x: x[0])

    if similarities:
        st.success("📑 Top 5 Plans Matched Based on Your Health Profile:")
        for sim, name, plan in similarities[:5]:
            company_username = plan.get("company_name", None)
            if company_username:
                user_query = db.collection("USERS").where("username", "==", company_username).stream()
                user_doc = next(user_query, None)
                if user_doc:
                    user_data = user_doc.to_dict()
                    csr = user_data.get('claim_settlement_ratio')
                    csr_text = f"{float(csr) * 100:.2f}%" if csr is not None else "N/A"
                    company_address = user_data.get('address', 'N/A')
                    med_conds = ('medical_condition')
                    diag_conds = plan.get('existing_diagnosis')

                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"""
                            <div class="card">
                                <h3>🛡 {name}</h3>
                                <p><strong>Match Score:</strong> {sim * 100:.2f}%</p>
                                <p><strong>Min Health Score:</strong> {plan.get('min_health_score')}</p>
                                <p><strong>Medical Conditions Covered:</strong> {med_conds}</p>
                                <p><strong>Existing Diagnoses Covered:</strong> {diag_conds}</p>
                                <hr style="margin: 10px 0;">
                                <p><strong>Company Name:</strong> {company_username}</p>
                                <p><strong>Email:</strong> {user_data.get('email', 'N/A')}</p>
                                <p><strong>Contact:</strong> {user_data.get('contact', 'N/A')}</p>
                                <p><strong>Address:</strong> {company_address}</p>
                                <p><strong>Claim Settlement Ratio:</strong> {csr_text}</p>
                            </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        geolocator = Nominatim(user_agent="insurance_map")
                        try:
                            location = geolocator.geocode(company_address, timeout=10)
                            if location:
                                m = folium.Map(location=[location.latitude, location.longitude], zoom_start=13)
                                folium.Marker([location.latitude, location.longitude], tooltip=company_username).add_to(m)
                                st_folium(m, width=350, height=250)
                            else:
                                st.warning("📍 Location not found")
                        except Exception as e:
                            st.error("🌐 Geolocation failed. Try again later.")
                else:
                    st.info("Company data not found.")
            else:
                st.info("Company name missing in plan data.")
    else:
        st.info("No matching plans found.")