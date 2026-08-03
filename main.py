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
    ["Add Expense", "View Expenses", "Search Expense", "Delete Expense", "Update Expense"]
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
# Delete Expense
elif menu == "Delete Expense":

    st.header("Delete Expense")

    df = pd.read_csv(FILE_NAME)

    if df.empty:
        st.info("No expenses available")
    else:
        st.dataframe(df)

        delete_date = st.text_input("Enter Date to Delete (DD-MM-YYYY)")

        if st.button("Delete Expense"):

            df = df[df["Date"] != delete_date]

            df.to_csv(FILE_NAME, index=False)

            st.success("Expense Deleted Successfully!")
# Update Expense
elif menu == "Update Expense":

    st.header("Update Expense")

    df = pd.read_csv(FILE_NAME)

    if df.empty:
        st.info("No expenses available")
    else:
        st.dataframe(df)

        update_date = st.text_input("Enter Date to Update (DD-MM-YYYY)")

        if update_date:
            result = df[df["Date"] == update_date]

            if not result.empty:
                category = st.text_input("New Category")
                description = st.text_input("New Description")
                amount = st.number_input("New Amount", min_value=0)

                if st.button("Update Expense"):

                    df.loc[df["Date"] == update_date, "Category"] = category
                    df.loc[df["Date"] == update_date, "Description"] = description
                    df.loc[df["Date"] == update_date, "Amount"] = amount

                    df.to_csv(FILE_NAME, index=False)

                    st.success("Expense Updated Successfully!")

            else:
                st.warning("Expense not found!")     