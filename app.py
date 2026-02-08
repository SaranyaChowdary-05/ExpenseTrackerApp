import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import re

# --- CONFIG ---
st.set_page_config(page_title="SpendWise AI", layout="wide")

# --- UTILS: VALIDATION ---
def validate_email(email):
    return email.endswith("@gmail.com")

def validate_password(password):
    # Min 6 chars, 1 Upper, 1 Lower, 1 Number, 1 Special Char
    if len(password) < 6:
        return False
    if not re.search("[a-z]", password): return False
    if not re.search("[A-Z]", password): return False
    if not re.search("[0-9]", password): return False
    if not re.search("[!@#$%^&*(),.?\\":{}|<>]", password): return False
    return True

# --- SESSION STATE INITIALIZATION ---
if 'users' not in st.session_state:
    st.session_state.users = {} # Format: {username: {password, fullname, email, budget}}
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# --- PAGE: HOME ---
if st.session_state.page == "Home":
    st.title("🚀 SpendWise AI")
    st.subheader("Smart Finance Tracking & Predictive Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### AI-Powered Budgeting")
        st.markdown("- **Forecasts:** Predicts trends.\n- **Control:** Set hard limits.\n- **Alerts:** Get notified when overspending.")
        if st.button("Login", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()
        if st.button("Register", use_container_width=True):
            st.session_state.page = "Register"
            st.rerun()
    with col2:
        st.image("https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&q=80&w=800")

# --- PAGE: REGISTRATION ---
elif st.session_state.page == "Register":
    st.title("📝 Create Account")
    with st.form("reg_form"):
        fname = st.text_input("Full Name")
        uname = st.text_input("Username")
        email = st.text_input("Email Address (must be @gmail.com)")
        phone = st.text_input("Phone Number")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        pwd = st.text_input("Create Password", type="password", help="Min 6 chars, 1 Upper, 1 Lower, 1 Number, 1 Special")
        cpwd = st.text_input("Confirm Password", type="password")
        
        submit = st.form_submit_button("Register")
        if submit:
            if uname in st.session_state.users:
                st.error("Username already exists!")
            elif not validate_email(email):
                st.error("Email must end with @gmail.com")
            elif not validate_password(pwd):
                st.error("Password must be 6+ chars with Upper, Lower, Number, and Special Char.")
            elif pwd != cpwd:
                st.error("Passwords do not match.")
            else:
                st.session_state.users[uname] = {"password": pwd, "name": fname, "budget": 0.0}
                st.success("Registration Successful! Please Login.")
                st.session_state.page = "Login"
                st.rerun()
    st.button("Back to Home", on_click=lambda: st.session_state.update({"page": "Home"}))

# --- PAGE: LOGIN ---
elif st.session_state.page == "Login":
    st.title("🔑 User Login")
    with st.form("login_form"):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if uname in st.session_state.users and st.session_state.users[uname]["password"] == pwd:
                if validate_password(pwd):
                    st.session_state.logged_in_user = uname
                    st.session_state.page = "Dashboard"
                    st.rerun()
                else:
                    st.error("Password does not meet security constraints.")
            else:
                st.error("Invalid Username or Password")
    st.button("Back to Home", on_click=lambda: st.session_state.update({"page": "Home"}))

# --- PAGE: DASHBOARD ---
elif st.session_state.page == "Dashboard":
    user = st.session_state.logged_in_user
    st.title(f"📊 Dashboard: Welcome {st.session_state.users[user]['name']}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.session_state.page = "Home"
        st.rerun()

    # Budget Setting
    st.subheader("⚙️ Manage Budget")
    new_budget = st.number_input("Set Monthly Expense Limit ($)", min_value=0.0, value=float(st.session_state.users[user]['budget']))
    st.session_state.users[user]['budget'] = new_budget

    # Expense Entry
    st.divider()
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.subheader("Add Expense")
        with st.form("exp_form"):
            item = st.text_input("Item")
            amt = st.number_input("Amount", min_value=0.0)
            if st.form_submit_button("Add Record"):
                st.session_state.expenses.append({"User": user, "Item": item, "Amount": amt})
                st.toast(f"Logged {item}")

    # Track & Manage
    with col_b:
        st.subheader("Expense Tracking")
        user_exps = [e for e in st.session_state.expenses if e['User'] == user]
        df = pd.DataFrame(user_exps)
        
        if not df.empty:
            total_spent = df['Amount'].sum()
            budget = st.session_state.users[user]['budget']
            
            # Metrics
            m1, m2 = st.columns(2)
            m1.metric("Total Spent", f"${total_spent:.2f}")
            m2.metric("Budget Limit", f"${budget:.2f}")
            
            # ALERT SYSTEM
            if total_spent > budget and budget > 0:
                st.error(f"⚠️ ALERT: You have exceeded your budget by ${total_spent - budget:.2f}!")
            elif total_spent > (budget * 0.8) and budget > 0:
                st.warning("🔔 Caution: You have reached 80% of your budget.")

            st.dataframe(df[['Item', 'Amount']], use_container_width=True)
        else:
            st.info("No expenses logged yet.")
