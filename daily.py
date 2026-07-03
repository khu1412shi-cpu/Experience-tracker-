import os
import pandas as pd
import streamlit as st

FILE_NAME = "expenses.txt"

# Page configuration for a professional look
st.set_page_config(page_title="Expense Tracker", layout="centered")


# Helper to load data safely
def load_data():
    if not os.path.exists(FILE_NAME) or os.stat(FILE_NAME).st_size == 0:
        return pd.DataFrame(columns=["Date", "Category", "Amount"])
    try:
        df = pd.read_csv(FILE_NAME, names=["Date", "Category", "Amount"])
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame(columns=["Date", "Category", "Amount"])


# Helper to save data
def save_data(df):
    df.to_csv(FILE_NAME, index=False, header=False)


# Initialize Data
df = load_data()

# App Title & Header
st.title("Smart Expense Tracker")
st.markdown(
    "A clean, efficient way to manage your daily finances. Built with Python and Streamlit."
)
st.divider()

# Sidebar Navigation
st.sidebar.header("Navigation")
menu = st.sidebar.radio(
    "Go to:", ["Dashboard & View", "Add Expense", "Delete Expense"]
)

# --- MENU 1: DASHBOARD & VIEW ---
if menu == "Dashboard & View":
    st.subheader("Financial Overview")

    if df.empty:
        st.info("No expenses recorded yet. Start by adding some!")
    else:
        # Key Metrics
        total_spent = df["Amount"].sum()
        total_items = len(df)

        col1, col2 = st.columns(2)
        col1.metric(label="Total Expenses", value=f"₹{total_spent:,.2f}")
        col2.metric(label="Total Transactions", value=total_items)

        st.divider()

        # Display Data Table
        st.subheader("Expense Logs")
        # Displaying with 1-based index matching your original logic
        display_df = df.copy()
        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True)


# --- MENU 2: ADD EXPENSE ---
elif menu == "Add Expense":
    st.subheader("Log a New Expense")

    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("Select Date").strftime("%d/%m/%Y")
        category = st.text_input("Category (e.g., Food, Rent, Fuel)")
        amount = st.number_input(
            "Amount (₹)", min_value=0.0, step=10.0, format="%.2f"
        )

        submit_btn = st.form_submit_form_button = st.form_submit_button(
            "Save Expense"
        )

        if submit_btn:
            if category.strip() == "" or amount <= 0:
                st.error("Please enter a valid category and amount.")
            else:
                # Append new row
                new_row = pd.DataFrame(
                    [[date, category, amount]],
                    columns=["Date", "Category", "Amount"],
                )
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("Expense Added Successfully!")
                st.balloons()


# --- MENU 3: DELETE EXPENSE ---
elif menu == "Delete Expense":
    st.subheader("Remove an Expense")

    if df.empty:
        st.info("No expenses available to delete.")
    else:
        # Formulate options for dropdown selection
        options = [
            f"{i+1}. {row['Date']} | {row['Category']} | ₹{row['Amount']}"
            for i, row in df.iterrows()
        ]
        selected_option = st.selectbox(
            "Select the expense you want to delete:", options
        )

        if st.button("Delete Selected Expense", type="primary"):
            # Get index from string option
            idx_to_delete = int(selected_option.split(".")[0]) - 1

            # Remove and Save
            df = df.drop(idx_to_delete).reset_index(drop=True)
            save_data(df)

            st.success("Expense Deleted Successfully!")
            st.rerun()

# Sidebar Footer
st.sidebar.divider()
st.sidebar.caption("Made with Streamlit")