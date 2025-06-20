import streamlit as st

def render_sidebar():
    # Hide Streamlit's default header, footer, and navigation
    hide_nav_style = """
        <style>
            header {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stSidebarNav"] {display: none;}
            .logout-button {
                background-color: #ff69b4 !important;
                color: white !important;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 20px;
                width: 100%;
                text-align: center;
            }
        </style>
    """
    st.markdown(hide_nav_style, unsafe_allow_html=True)

    # Check for login and type
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("Unauthorized access.")
        st.stop()

    user_type = st.session_state.get("user_type")

    if user_type == "Individual":
        st.sidebar.title("🧍 Individual Menu")
        st.sidebar.page_link("pages/user_upload_docs.py", label="📤 Diagnosis Report")
        st.sidebar.page_link("pages/user_lab_reports.py", label="🧪 Medical Test")
        st.sidebar.page_link("pages/user_lifestyle.py", label="🏃 Lifestyle Tracker")
        st.sidebar.page_link("pages/user_sum_value.py", label="➕ Existing Policy")
        st.sidebar.page_link("pages/user_suggest_insurance.py", label="➕ Best Insurance Plans")

    elif user_type == "Company":
        st.sidebar.title("🏢 Company Menu")
        st.sidebar.page_link("pages/company_dashboard.py", label="📊 Company Dashboard")
        st.sidebar.page_link("pages/company_insurance.py", label="💼 Insurance")
        st.sidebar.page_link("pages/company_showplans.py", label="➕ View Plans")
        st.sidebar.page_link("pages/company_lifestyle.py", label="🧬 Lifestyle Analysis")
    else:
        st.error("Unknown user type.")
        st.stop()

    # === Logout Button ===
    if st.sidebar.button("🚪 Logout", key="logout_button"):
        st.session_state.clear()
        st.switch_page("app.py")