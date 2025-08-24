import streamlit as st
from analytics_ui import analytics_tab
from add_update_ui import add_update_tab
from analytics_months import analytics_months_tab

API_URL = "http://localhost:8000"

st.title("Expense Tracking System")

tab1,tab2,tab3 = st.tabs(["Add/Update","Analytics by Category","Analytics by Months"])
with tab1:
    add_update_tab()

with tab2:
    analytics_tab()
with tab3:
    analytics_months_tab()
