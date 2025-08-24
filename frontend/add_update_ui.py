
import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
    selected_date = st.date_input(
        "Enter Date:", datetime(2024, 8, 1), label_visibility="collapsed"
    )

    # Fetch existing expenses for the selected date
    response = requests.get(f"{API_URL}/expenses/{selected_date.strftime('%Y-%m-%d')}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Something went wrong while fetching existing expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # Form to input expenses
    with st.form(key="expenses_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        expenses = []
        for i in range(5):
            # Pre-fill existing expenses if available
            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"] or ""
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                number_input = st.number_input(
                    label="Amount",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label="Notes",
                    value=notes,
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                "amount": number_input,
                "category": category_input,
                "notes": notes_input
            })

        submit_button = st.form_submit_button("Submit")

    # Submit expenses one by one
    if submit_button:
        filtered_expenses = [exp for exp in expenses if exp["amount"] > 0]
        success_count = 0

        for expense in filtered_expenses:
            payload = {
                "expense_date": selected_date.strftime("%Y-%m-%d"),
                "amount": expense["amount"],
                "category": expense["category"],
                "notes": expense["notes"]
            }
            try:
                response = requests.post(f"{API_URL}/expenses/", json=payload)
                if response.status_code == 200:
                    success_count += 1
                else:
                    st.error(f"Failed to submit expense: {expense}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

        if success_count == len(filtered_expenses):
            st.success("Expenses successfully updated")
        elif success_count > 0:
            st.warning(f"{success_count} of {len(filtered_expenses)} expenses were saved")
        else:
            st.error("No expenses were saved")

