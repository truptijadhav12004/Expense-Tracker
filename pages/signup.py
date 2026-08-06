import streamlit as st
from pymongo import MongoClient

# ---------------- MongoDB ----------------
MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)

db = client["ExpenseTrackerDB"]

users = db["users"]


st.set_page_config(
    page_title="Sign Up",
    page_icon="👤",
    layout="centered"
)


# ---------- Title ----------
st.markdown(
    """
    <h1 style='text-align:center; color:#16a34a;'>
        💰 Smart Expense Tracker
    </h1>
    <h3 style='text-align:center; color:#555;'>
        👤 Create Your Account
    </h3>
    <hr>
    """,
    unsafe_allow_html=True
)


# ---------- Signup Form ----------
with st.container():

    name = st.text_input(
        "👤 Full Name",
        placeholder="Enter your full name"
    )

    email = st.text_input(
        "📧 Email Address",
        placeholder="Enter your email"
    )

    mobile = st.text_input(
        "📱 Mobile Number",
        placeholder="Enter your mobile number"
    )

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    confirm_password = st.text_input(
        "🔒 Confirm Password",
        type="password"
    )


    if st.button("✅ Create Account", use_container_width=True):

        if (
            not name.strip()
            or not email.strip()
            or not mobile.strip()
            or not password.strip()
            or not confirm_password.strip()
        ):
            st.error("⚠️ Please fill all fields.")

        elif password != confirm_password:
            st.error("❌ Passwords do not match.")

        elif users.find_one({"email": email}):
            st.warning("⚠️ Email already registered.")

        else:

            users.insert_one(
                {
                    "name": name,
                    "email": email,
                    "mobile": mobile,
                    "password": password
                }
            )

            st.success("✅ Account Created Successfully!")

            st.switch_page("pages/login.py")