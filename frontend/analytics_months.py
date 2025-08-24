
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

API_URL = "http://localhost:8000"

def fill_missing_months(data_dict, start_date, end_date):
    """
    Ensure every month between start_date and end_date exists in the dict.
    Missing months are filled with 0.
    """
    result = {}
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while current <= end:
        month_str = current.strftime("%Y-%m")
        result[month_str] = data_dict.get(month_str, 0)
        current += relativedelta(months=1)

    return result

def analytics_months_tab():
    st.header("Monthly Expenses Summary")

    # Tab 3 inputs for start/end date
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date ", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date ", datetime(2024, 8, 2))

    if st.button("Get Monthly Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }

        try:
            response = requests.post(f"{API_URL}/monthly_expenses", json=payload)
            response.raise_for_status()
            data = response.json()

            # Fill missing months with 0
            data = fill_missing_months(data, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

            # Convert dict to DataFrame
            df = pd.DataFrame(list(data.items()), columns=["MonthCode", "Total"])

            # Convert "YYYY-MM" to "Month Year" format
            df["Month"] = pd.to_datetime(df["MonthCode"]).dt.strftime("%B %Y")
            df = df[["Month", "Total"]]  # reorder columns

            # Show bar chart
            st.subheader("Expenses by Month")
            st.bar_chart(df.set_index("Month")["Total"])

            # Show table too
            st.subheader("Monthly Table")
            st.table(df)

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching monthly expenses: {e}")
