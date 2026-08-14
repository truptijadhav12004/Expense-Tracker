import streamlit as st
from pymongo import MongoClient


# ---------------- Page Settings ----------------

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)


# ---------------- MongoDB ----------------

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)

db = client["ExpenseTrackerDB"]

users = db["users"]


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


    # ---------------- Login Button ----------------

    if st.button("🔐 Login"):

        # Check whether email is registered
        registered_user = users.find_one(
            {"email": email}
        )

        if not registered_user:

            st.warning("⚠️ Please Sign Up First!")
            st.info(
                "New user? Please create an account before logging in."
            )

        else:

            # Check email and password
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

                st.error("❌ Invalid Password.")