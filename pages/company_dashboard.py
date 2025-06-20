import streamlit as st
import sidebar

st.set_page_config(
    page_title="Insurance Admin Dashboard",
    layout="wide",
)

sidebar.render_sidebar()

# Custom CSS for professional purple-pink theme and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    /* Page background */
    .main {
        background: linear-gradient(135deg, #8e2de2, #f9a8d4);
        min-height: 100vh;
        font-family: 'Poppins', sans-serif;
        color: #33004d;
        padding: 1rem 2rem 3rem 2rem;
    }

    /* Dashboard Title */
    .dashboard-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #5e2ca5;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 3px #c47aff;
    }

    /* Tab Buttons Container */
    .tab-buttons {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        margin-bottom: 2.5rem;
    }

    /* Tab Buttons */
    .tab-button {
        background: #a85afc;
        border: none;
        padding: 0.7rem 2rem;
        border-radius: 40px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(168, 90, 252, 0.5);
        transition: background-color 0.3s ease, transform 0.2s ease;
        font-size: 1.1rem;
    }

    .tab-button:hover {
        background: #f274b7;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(242, 116, 183, 0.6);
    }

    .tab-button.active {
        background: #f15bb5;
        box-shadow: 0 6px 18px rgba(241, 91, 181, 0.8);
        cursor: default;
        transform: none;
    }

    /* Remove default form styling to align buttons inline */
    form {
        margin: 0;
        display: inline-block;
    }

    /* Cards Container */
    .card-container {
        display: flex;
        justify-content: center;
        gap: 2.5rem;
        flex-wrap: wrap;
    }

    /* Individual Cards */
    .card {
        background: #fff0ff;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(168, 90, 252, 0.25);
        padding: 2rem 3rem;
        width: 220px;
        text-align: center;
        color: #4b007d;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(168, 90, 252, 0.45);
    }

    .card-icon {
        font-size: 3.5rem;
        margin-bottom: 0.8rem;
    }

    .card-label {
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
    }

    .card-value {
        font-weight: 600;
        font-size: 1.8rem;
        color: #8e2de2;
    }
</style>
""", unsafe_allow_html=True)

# Wrap all content inside a main div to apply background and font globally
# st.markdown('<div class="main">', unsafe_allow_html=True)

# ---------- Dashboard Title ----------
st.markdown('<div class="dashboard-title">Insurance Admin Dashboard</div>', unsafe_allow_html=True)

# ---------- Tab Buttons ----------
# st.markdown("""
# <div class="tab-buttons">
#     <button class="tab-button active" disabled>Overview</button>
#     <form action="/Insurances" method="get">
#         <button class="tab-button" type="submit">Insurances</button>
#     </form>
#     <form action="/Add" method="get">
#         <button class="tab-button" type="submit">Add</button>
#     </form>
#     <form action="/Lifestyle" method="get">
#         <button class="tab-button" type="submit">Lifestyle</button>
#     </form>
# </div>
# """, unsafe_allow_html=True)

# ---------- Info Cards ----------
st.markdown("""
<div class="card-container">
    <div class="card">
        <div class="card-icon">💲</div>
        <div class="card-label">Total Revenue</div>
        <div class="card-value">82,000</div>
    </div>
    <div class="card">
        <div class="card-icon">👥</div>
        <div class="card-label">Total Customers</div>
        <div class="card-value">7</div>
    </div>
    <div class="card">
        <div class="card-icon">🛡</div>
        <div class="card-label">Active Policies</div>
        <div class="card-value">11</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
