import streamlit as st
import sidebar
sidebar.render_sidebar()

# === Load External CSS ===
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("userstyle.css")

# === Custom CSS for Theme + Animations ===
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Rubik', sans-serif;
            background: linear-gradient(135deg, #d993f5, #fcb1c5);
            color: #4b007d;
            animation: fadeIn 1.2s ease-in;
        }

        .block-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 1.2rem;
            padding: 2rem 3rem;
            margin-top: 2rem;
            box-shadow: 0 8px 30px rgba(183, 78, 165, 0.25);
            animation: fadeIn 1.5s ease-in-out;
        }

        h2, h3, .stSubheader {
            color: #6a0dad;
            font-weight: 600;
            animation: slideUp 1s ease-in-out;
        }

        label {
            font-weight: 600;
            color: #7a1faf;
        }

        input, .stNumberInput > div > input {
            border-radius: 8px !important;
            border: 1.8px solid #b76ba3 !important;
            padding: 8px;
            font-weight: 500;
            color: #4b007d !important;
        }

        .stButton > button {
            background-color: #9b30ff;
            color: white;
            font-weight: 600;
            padding: 0.6rem 1.5rem;
            border-radius: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(155, 48, 255, 0.5);
            animation: bounceUp 1s ease-in-out;
        }

        .stButton > button:hover {
            background-color: #7a1fff;
            box-shadow: 0 5px 15px rgba(122, 31, 255, 0.7);
            transform: scale(1.05);
        }

        .stAlert {
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            animation: fadeIn 1.2s ease-in-out;
        }

        .success {
            background-color: #e0c3fc !important;
            border-left: 6px solid #9b30ff !important;
        }

        .error {
            background-color: #fcd0e5 !important;
            border-left: 6px solid #d42f6f !important;
        }

        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }

        @keyframes slideUp {
            0% {transform: translateY(30px); opacity: 0;}
            100% {transform: translateY(0); opacity: 1;}
        }

        @keyframes bounceUp {
            0% {transform: scale(0.9); opacity: 0;}
            60% {transform: scale(1.05); opacity: 1;}
            100% {transform: scale(1);}
        }
    </style>
""", unsafe_allow_html=True)

# === Page Title ===
st.markdown('<h2 style="text-align:center; margin-bottom: 1.5rem;">💜 Calculate Your Eligible Sum Assured</h2>', unsafe_allow_html=True)
st.markdown("Provide your details below to estimate the maximum sum assured you qualify for.")

# === User Inputs ===
age = st.number_input("Age (years)", min_value=0, help="Enter your current age")
annual_income = st.number_input("Annual Income (₹)", min_value=0, help="Enter your total annual income")
policy_value = st.number_input("Value of Existing Policies (₹)", min_value=0, help="Sum of your current insurance policies' values")

# === Calculate Button and Result ===
if st.button("Calculate Eligible Sum"):
    if age < 20:
        st.error("⚠ Age must be 20 or above to calculate eligibility.")
    elif annual_income == 0:
        st.error("⚠ Please enter a valid Annual Income.")
    else:
        if 20 <= age <= 30:
            sum_assured = (annual_income * 12) - policy_value
        elif 31 <= age <= 55:
            sum_assured = (annual_income * 7) - policy_value
        else:
            sum_assured = (annual_income * 4) - policy_value

        sum_assured = max(0, sum_assured)
        st.success(f"🎉 Your Eligible Sum Assured Value is: *₹{sum_assured:,.2f}*")