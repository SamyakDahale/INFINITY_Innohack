import streamlit as st
import upload_docs
import lab_reports
import manual_entry
import sum_value

st.set_page_config(page_title="Health Profile Dashboard", layout="centered")

# === Load External CSS ===
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styleapp.css")  # Or "styles/style.css" if in a subfolder

# === Header ===
st.markdown("<h1>Health Profile Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p>Lorem welcome</p>", unsafe_allow_html=True)

# === Navigation Buttons ===
cols = st.columns(5)

if "page" not in st.session_state:
    st.session_state.page = "upload"

button_labels = {
    "upload": "Upload Docs",
    "lab": "Lab Reports",
    "manual": "Manual Entry",
    "lifestyle": "Lifestyle",
    "sum": "Sum Value"
}

button_keys = list(button_labels.keys())

for i, key in enumerate(button_keys):
    with cols[i]:
        if st.session_state.page == key:
            if st.button(button_labels[key], key=key, help=button_labels[key]):
                st.session_state.page = key
            st.markdown(
                f"""<script>
                const btn = window.document.querySelectorAll('button[data-testid="baseButton-{key}"]')[0];
                if(btn) btn.parentElement.classList.add("button-active");
                </script>""",
                unsafe_allow_html=True
            )
        else:
            if st.button(button_labels[key], key=key, help=button_labels[key]):
                st.session_state.page = key

st.markdown("---")

# === Render Pages Dynamically ===
if st.session_state.page == "upload":
    upload_docs.show()
elif st.session_state.page == "lab":
    lab_reports.show()
elif st.session_state.page == "manual":
    manual_entry.show()
elif st.session_state.page == "lifestyle":
    lifestyle.show()
elif st.session_state.page == "sum":
    sum_value.show()
