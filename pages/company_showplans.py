import streamlit as st
import sidebar
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from io import StringIO
import json

# Sidebar
sidebar.render_sidebar()

# Only initialize Firebase if not already initialized
if not firebase_admin._apps:
    # Load credentials from Streamlit secrets
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Custom CSS styling
st.markdown("""
    <style>
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 1rem;
        }
        .dataframe th, .dataframe td {
            text-align: center;
            padding: 10px;
        }
        .dataframe {
            border: 1px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
        }
        .stDataFrame div[data-testid="dataTableContainer"] {
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
        .badge {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
            margin: 2px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📋 Your Insurance Plans (Tabular View)")

# Check login
if "username" not in st.session_state or st.session_state.get("user_type") != "Company":
    st.warning("Please log in as a company to view your insurance plans.")
    st.stop()

company_username = st.session_state.username

# Fetch plans where 'company' matches username
plans_ref = db.collection("INSURANCE_PLANS").where("company_name", "==", company_username)
plans = plans_ref.stream()

# Collect data into list
plans_data = []
for plan in plans:
    data = plan.to_dict()
    plans_data.append({
        "Insurance Name": data.get("insurance_name", ""),
        "Premium (₹/10L)": data.get("premium", 0),
        "Min Health Score": data.get("min_health_score", 0),
        "Medical Condition": data.get("medical_condition", ""),
        "Pre-existing Diagnosis": data.get("existing_diagnosis", ""),
        "Add-ons": data.get("addons", ""),
        "Description": data.get("description", "")
    })

# Display in table
if plans_data:
    df = pd.DataFrame(plans_data)
    
    # Display table with HTML rendering for styled Add-ons
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # Download CSV button
    csv_df = pd.DataFrame(plans_data)
    csv_df["Add-ons"] = csv_df["Add-ons"].str.replace('<[^<]+?>', '', regex=True)  # remove HTML tags for clean CSV
    csv = csv_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download as CSV", data=csv, file_name="insurance_plans.csv", mime="text/csv")

    # Plot chart
    st.subheader("📊 Premium vs Min Health Score")
    chart_df = csv_df.copy()
    chart_df["Premium (₹/10L)"] = pd.to_numeric(chart_df["Premium (₹/10L)"], errors='coerce')
    chart_df["Min Health Score"] = pd.to_numeric(chart_df["Min Health Score"], errors='coerce')

        # Add a constant column for fixed bubble size
    chart_df["Dot Size"] = 15 # you can increase this to 30 or 40 if needed

    fig = px.scatter(chart_df, 
                    x="Min Health Score", 
                    y="Premium (₹/10L)",
                    size="Dot Size",  # Fixed size for all dots
                    hover_name="Insurance Name",
                    color="Medical Condition",
                    title="Premium vs Health Score",
                    labels={"Min Health Score": "Health Score", "Premium (₹/10L)": "Premium (₹/10L)"})

    st.plotly_chart(fig, use_container_width=True)