import streamlit as st
import sidebar
import re
import io
import numpy as np
import pickle
from PIL import Image

# Load model and tools
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("label_encoder.pkl", "rb") as le_file:
    label_encoder = pickle.load(le_file)
with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

sidebar.render_sidebar()

# Apply custom theme + working motion
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to right, #ffccff, #e0b3ff);
            color: #4b0082;
        }

        .block-container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem 3rem;
            border-radius: 1.5rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
            animation: fadeIn 1.2s ease-in-out;
        }

        .fade-in {
            animation: fadeIn 1.2s ease-in-out;
        }

        .slide-up {
            animation: slideUp 0.8s ease-in-out;
        }

        .stTextInput input {
            border: 2px solid #d19fe8;
            border-radius: 12px;
            padding: 10px;
        }

        .stButton > button {
            background-color: #da70d6;
            color: white;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            border-radius: 10px;
            border: none;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #c71585;
            transform: scale(1.05);
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        @keyframes slideUp {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# === Extraction Functions ===
def extract_text_from_pdf(file_bytes):
    import fitz
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    return "".join(page.get_text() for page in doc)

def extract_text_from_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PDF')
    return extract_text_from_pdf(img_byte_arr.getvalue())

# === Medical Regex ===
TESTS = ["Blood Glucose", "HbA1C", "Systolic BP", "Diastolic BP", "LDL", "HDL", "Triglycerides", "Haemoglobin", "MCV"]
PATTERN = r"(?i)({})[^\d]+([\d]+(?:\.\d+)?)".format("|".join(TESTS))

def extract_medical_values(text):
    extracted = {}
    matches = re.findall(PATTERN, text)
    for key, value in matches:
        extracted[key.strip()] = float(value)
    return extracted

# === ML Logic ===
def predict_disease(values):
    EXPECTED = ["Blood Glucose", "HbA1C", "Systolic BP", "Diastolic BP", "LDL", "HDL", "Triglycerides", "Haemoglobin", "MCV"]
    features = [values.get(test, 0.0) for test in EXPECTED]
    features = np.array([features]).astype(float)
    scaled = scaler.transform(features)
    encoded = model.predict(scaled)[0]
    return label_encoder.inverse_transform([encoded])[0]

# === UI Layout ===
st.markdown('<div class="fade-in"><h2>💜 Personal Health Assessment Portal</h2></div>', unsafe_allow_html=True)
st.markdown('<div class="slide-up">Enter your health parameters manually or upload a diagnostic report for automatic analysis.</div>', unsafe_allow_html=True)

manual_values = {}
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
for test in TESTS:
    manual_values[test] = st.text_input(f"🔬 {test}")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="fade-in"><h4>📎 Upload Report (PDF or Image)</h4></div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drop your test report here", type=["pdf", "jpg", "jpeg"])

if st.button("🧠 Analyze Health Data"):
    all_values = {}

    for k, v in manual_values.items():
        if v:
            try:
                all_values[k] = float(v)
            except:
                st.warning(f"⚠ Please enter a valid number for {k}")

    if uploaded_file:
        file_bytes = uploaded_file.read()
        extracted_text = None
        try:
            if uploaded_file.name.endswith(".pdf"):
                extracted_text = extract_text_from_pdf(file_bytes)
            else:
                extracted_text = extract_text_from_image(file_bytes)
        except:
            st.error("❌ Error reading the uploaded file.")

        if extracted_text:
            parsed_values = extract_medical_values(extracted_text)
            st.markdown('<div class="fade-in"><h4>🧾 Extracted Medical Values:</h4></div>', unsafe_allow_html=True)
            st.json(parsed_values)
            all_values.update(parsed_values)

    if all_values:
        prediction = predict_disease(all_values)
        st.markdown(f'<div class="slide-up"><h3>🧬 Likely Medical Condition Detected: <strong>{prediction}</strong></h3></div>', unsafe_allow_html=True)
        st.session_state.medical_conditions = prediction
    else:
        st.warning("Please fill in values or upload a valid report.")