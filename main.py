import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import date


# ---------------- Page Settings ----------------

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# ---------------- Login Protection ----------------

if not st.session_state.get("logged_in", False):

    st.warning("⚠️ Please Login First")

    st.switch_page("pages/login.py")


# ---------------- MongoDB ----------------

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)

db = client["ExpenseTrackerDB"]

collection = db["expenses"]
# ---------------- Page ----------------
st.markdown(
    """
    <h1 style='text-align:center;color:#16a34a;'>
    💰 Smart Expense Tracker
    </h1>
    <h4 style='text-align:center;color:gray;'>
    Track • Analyze • Save Money
    </h4>
    <hr>
    """,
    unsafe_allow_html=True
)
# ---------------- Sidebar ----------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2331/2331941.png", width=80)

st.sidebar.title("💰 Expense Tracker")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "📋 Select Option",
    [
        "🏠 Dashboard",
        "➕ Add Expense",
        "📋 View Expenses",
        "🔍 Search Expense",
        "✏️ Update Expense",
        "🗑️ Delete Expense"
    ]
)

# ---------------- Dashboard ----------------
if menu == "🏠 Dashboard":

    st.subheader("📊 Dashboard")

    data = list(collection.find({}, {"_id": 0}))

    if data:

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    format="mixed"
).dt.strftime("%d-%b-%Y")

        total_expense = df["Amount"].sum()
        total_records = len(df)
        total_categories = df["Category"].nunique()
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#16a34a,#22c55e);
                        padding:25px;
                        border-radius:15px;
                        box-shadow:0 4px 12px rgba(0,0,0,0.25);
                        text-align:center;">
                <h3 style="color:white;">💰 Total Expense</h3>
                <h1 style="color:white;font-size:42px;">₹ {total_expense:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#2563eb,#3b82f6);
                        padding:25px;
                        border-radius:15px;
                        box-shadow:0 4px 12px rgba(0,0,0,0.25);
                        text-align:center;">
                <h3 style="color:white;">📂 Categories</h3>
                <h1 style="color:white;font-size:42px;">{total_categories}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#ea580c,#f97316);
                        padding:25px;
                        border-radius:15px;
                        box-shadow:0 4px 12px rgba(0,0,0,0.25);
                        text-align:center;">
                <h3 style="color:white;">📝 Records</h3>
                <h1 style="color:white;font-size:42px;">{total_records}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("🕒 Recent Expenses")
        st.dataframe(df.tail(5), use_container_width=True)

        st.subheader("📊 Expense by Category")
        chart = df.groupby("Category")["Amount"].sum()
        st.bar_chart(chart)

    else:
        st.info("No Expenses Found")

        
# ---------------- Add Expense ----------------
elif menu == "➕ Add Expense":

    st.subheader("➕ Add New Expense")

    expense_date = st.date_input("📅 Select Date")

    category = st.selectbox(
        "📂 Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Medical",
            "Education",
            "Bills",
            "Other"
        ]
    )

    description = st.text_input("📝 Description")

    amount = st.number_input(
        "💰 Amount",
        min_value=0
    )

    if st.button("✅ Add Expense"):

        collection.insert_one({
            "Date": str(expense_date),
            "Category": category,
            "Description": description,
            "Amount": amount
        })

        st.success("Expense Added Successfully ✅")
       # ---------------- View Expenses ----------------
elif menu == "📋 View Expenses":

    st.subheader("📋 All Expenses")

    data = list(collection.find({}, {"_id": 0}))

    if data:

        df = pd.DataFrame(data)

        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Expense by Category")

        chart = df.groupby("Category")["Amount"].sum()

        st.bar_chart(chart)

    else:
        st.warning("No Expenses Found")


# ---------------- Search Expense ----------------
elif menu == "🔍 Search Expense":

    st.subheader("🔍 Search Expense")

    search_date = st.date_input("📅 Select Date")

    if st.button("🔍 Search"):

        data = list(
            collection.find(
                {"Date": str(search_date)},
                {"_id": 0}
            )
        )

        if data:
            st.success(f"{len(data)} Record(s) Found")
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.warning("No Expense Found")


# ---------------- Update Expense ----------------
elif menu == "✏️ Update Expense":

    st.subheader("✏️ Update Expense")

    update_date = st.date_input("📅 Select Date")

    new_category = st.selectbox(
        "New Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Medical",
            "Education",
            "Bills",
            "Other"
        ]
    )

    new_description = st.text_input("New Description")

    new_amount = st.number_input(
        "New Amount",
        min_value=0.0
    )

    if st.button("✏️ Update Expense"):

        result = collection.update_one(
            {"Date": str(update_date)},
            {
                "$set": {
                    "Category": new_category,
                    "Description": new_description,
                    "Amount": new_amount
                }
            }
        )

        if result.modified_count > 0:
            st.success("✅ Expense Updated Successfully")
        else:
            st.warning("Expense Not Found")


# ---------------- Delete Expense ----------------
elif menu == "🗑️ Delete Expense":

    st.subheader("🗑️ Delete Expense")

    delete_date = st.date_input("📅 Select Date")

    if st.button("🗑️ Delete Expense"):

        result = collection.delete_one(
            {"Date": str(delete_date)}
        )

        if result.deleted_count > 0:
            st.success("🗑️ Expense Deleted Successfully")
        else:
            st.warning("Expense Not Found")