import streamlit as st
import pandas as pd
import os

FILE_NAME = "expenses.csv"

# Create CSV file if not exists
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])
    df.to_csv(FILE_NAME, index=False)

st.title("💰 Expense Tracker System")

menu = st.sidebar.selectbox(
    "Select Option",
    ["Add Expense", "View Expenses", "Search Expense"]
)

# Add Expense
if menu == "Add Expense":

    st.header("Add New Expense")

    date = st.text_input("Enter Date (DD-MM-YYYY)")
    category = st.text_input("Enter Category")
    description = st.text_input("Enter Description")
    amount = st.number_input("Enter Amount", min_value=0)

    if st.button("Add Expense"):
        df = pd.read_csv(FILE_NAME)

        new_expense = pd.DataFrame({
            "Date": [date],
            "Category": [category],
            "Description": [description],
            "Amount": [amount]
        })

        df = pd.concat([df, new_expense], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)

        st.success("Expense Added Successfully!")


# View Expense
elif menu == "View Expenses":

    st.header("Expense List")

    df = pd.read_csv(FILE_NAME)

    if df.empty:
        st.info("No expenses found")
    else:
        st.dataframe(df)


# Search Expense
elif menu == "Search Expense":

    st.header("Search Expense")

    category = st.text_input("Enter Category")

    if st.button("Search"):

        df = pd.read_csv(FILE_NAME)

        result = df[df["Category"].str.lower() == category.lower()]

        if result.empty:
            st.warning("No expense found")
        else:
            st.dataframe(result)
