

import streamlit as st
import sidebar
sidebar.render_sidebar()



st.title("👤 Individual User Dashboard")
st.write(f"Welcome, {st.session_state.get('username', 'Guest')}!")
