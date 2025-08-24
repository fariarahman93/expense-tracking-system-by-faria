
import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"  # ✅ backend

def analytics_tab():
    st.header("Analytics by Category")

    # Date inputs
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1), label_visibility="collapsed")
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5), label_visibility="collapsed")

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }

        try:
            response = requests.post(f"{API_URL}/analytics/", json=payload)
            response.raise_for_status()
            data = response.json()

            if not data:
                st.info("No analytics data found for this range.")
                return

            # ✅ Store results for Tab3
            st.session_state.analytics_data = data
            st.session_state.tab2_start_date = start_date
            st.session_state.tab2_end_date = end_date

            # Convert response to DataFrame
            df = pd.DataFrame([
                {"Category": cat, "Total": data[cat]["total"], "Percentage": data[cat]["percentage"]}
                for cat in data
            ])

            # Sort categories by total
            df_sorted = df.sort_values("Total", ascending=False)

            # Show chart
            st.subheader("Expense Breakdown by Category")
            st.bar_chart(df_sorted.set_index("Category")["Percentage"])

            # Show table
            st.subheader("Category-wise Table")
            st.table(df_sorted)

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching analytics: {e}")

