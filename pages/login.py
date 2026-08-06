import streamlit as st
from pymongo import MongoClient


# ---------------- MongoDB ----------------

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)

db = client["ExpenseTrackerDB"]

users = db["users"]


# ---------------- Page Settings ----------------

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)


# ---------------- Title ----------------

st.title("🔐 Login Page")


# ---------------- Login Form ----------------

with st.container():

    email = st.text_input(
        "📧 Email Address",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "🔒 Password",
        type="password"
    )


    if st.button("🔐 Login"):

        user = users.find_one(
            {
                "email": email,
                "password": password
            }
        )


        if user:

            st.success("✅ Login Successful!")

            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["user_name"] = user["name"]

            st.switch_page("main.py")


        else:

            st.error("❌ Invalid Email or Password.")