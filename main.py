import streamlit as st
import pandas as pd
import os
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://truptijadhav12004_db_user:trupti12345@cluster0.ur9fmgq.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["ExpenseTrackerDB"]
collection = db["expenses"]

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

        collection.insert_one({
            "Date": date,
            "Category": category,
            "Description": description,
            "Amount": amount
        })

        st.success("Expense Added Successfully!")
# View Expenses
elif menu == "View Expenses":

    st.header("Expense List")

    data = list(collection.find({}, {"_id": 0}))

    if len(data) == 0:
        st.info("No expenses found")
    else:
        df = pd.DataFrame(data)
        st.dataframe(df)

# Search Expense
elif menu == "Search Expense":

    st.header("Search Expense")

    search_date = st.text_input("Enter Date to Search")

    if st.button("Search"):

        data = list(collection.find({"Date": search_date}, {"_id": 0}))

        if len(data) == 0:
            st.warning("No expense found")
        else:
            df = pd.DataFrame(data)
            st.dataframe(df)


# Delete Expense
elif menu == "Delete Expense":

    st.header("Delete Expense")

    delete_date = st.text_input("Enter Date to Delete")

    if st.button("Delete"):

        result = collection.delete_one({"Date": delete_date})

        if result.deleted_count > 0:
            st.success("Expense deleted successfully")
        else:
            st.warning("Expense not found")
# Update Expense
elif menu == "Update Expense":

    st.header("Update Expense")

    update_date = st.text_input("Enter Date to Update")

    new_category = st.text_input("New Category")
    new_description = st.text_input("New Description")
    new_amount = st.number_input("New Amount", min_value=0)

    if st.button("Update"):

        result = collection.update_one(
            {"Date": update_date},
            {
                "$set": {
                    "Category": new_category,
                    "Description": new_description,
                    "Amount": new_amount
                }
            }
        )

        if result.modified_count > 0:
            st.success("Expense updated successfully")
        else:
            st.warning("Expense not found")