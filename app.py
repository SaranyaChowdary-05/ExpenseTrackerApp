import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import re

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="SpendWise AI", layout="wide")

# --- 2. SECURITY CONSTRAINTS ---
def validate_email(email):
    return email.lower().endswith("@gmail.com")

def validate_password(password):
    # Constraint: 6+ chars, 1 Upper, 1 Lower, 1 Number, 1 Special Char
    if len(password) < 6:
        return False
    if not re.search(r"[a-z]", password): return False
    if not re.search(r"[A-Z]", password): return False
    if not re.search(r"[0-9]", password): return False
    # Rectified Regex string using single quotes to avoid SyntaxError
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password): return False
    return True

# --- 3. SESSION STATE (MOCK DATABASE) ---
if 'users' not in st.session_state:
    st.session_state.users = {} # {username: {password, name, budget, expenses: []}}
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"

def nav(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 4. NAVIGATION LOGIC ---

# HOME PAGE
if st.session_state.page == "Home":
    st.title("🚀 SpendWise AI")
    st.subheader("Smart Finance Tracking with Predictive Alerts")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### AI-Powered Budgeting")
        st.markdown("- **Strict Validation:** Secure login and registration.\n- **Budget Limits:** Set and manage your spending caps.\n- **Real-time Alerts:** Notifications before you overspend.")
        if st.button("Login", use_container_width=True): nav("Login")
        if st.button("Register", use_container_width=True): nav("Register")
    with col2:
        st.image("https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&q=80&w=800")

# REGISTRATION PAGE
elif st.session_state.page == "Register":
    st.title("📝 Create Account")
    with st.form("reg_form"):
        f_name = st.text_input("Full Name")
        u_name = st.text_input("Username")
        email = st.text_input("Email Address (@gmail.com only)")
        phone = st.text_input("Phone Number")
        gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
        p1 = st.text_input("Create Password", type="password")
        p2 = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Sign Up"):
            if u_name in st.session_state.users:
                st.error("Username already exists.")
            elif not validate_email(email):
                st.error("Email must be a @gmail.com address.")
            elif not validate_password(p1):
                st.error("Password must be 6+ chars with Upper, Lower, Number, and Special Symbol.")
            elif p1 != p2:
                st.error("Passwords do not match.")
            else:
                st.session_state.users[u_name] = {
                    "password": p1, "name": f_name, "budget": 0.0, "expenses": []
                }
                st.success("Account created! Redirecting to login...")
                nav("Login")
    st.button("Back", on_click=lambda: nav("Home"))

# LOGIN PAGE
elif st.session_state.page == "Login":
    st.title("🔑 Secure Login")
    with st.form("login_form"):
        u_name = st.text_input("Username")
        p_word = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if u_name in st.session_state.users and st.session_state.users[u_name]["password"] == p_word:
                if validate_password(p_word): # Constraint check on login
                    st.session_state.logged_in_user = u_name
                    nav("Dashboard")
                else:
                    st.error("Your password is insecure. Please reset it to match requirements.")
            else:
                st.error("Invalid credentials.")
    st.button("Back", on_click=lambda: nav("Home"))

# DASHBOARD PAGE
elif st.session_state.page == "Dashboard":
    user = st.session_state.logged_in_user
    u_data = st.session_state.users[user]
    
    st.sidebar.title(f"Hello, {u_data['name']}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        nav("Home")

    st.title("📊 Personal Expense Dashboard")
    
    # BUDGET MANAGEMENT
    st.subheader("💰 Budget Settings")
    budget = st.number_input("Set your Monthly Budget Limit ($)", min_value=0.0, value=float(u_data['budget']))
    u_data['budget'] = budget

    st.divider()

    # EXPENSE TRACKER
    col_in, col_disp = st.columns([1, 2])
    
    with col_in:
        st.write("### Add Expense")
        with st.form("expense_add"):
            item = st.text_input("Description")
            amt = st.number_input("Amount ($)", min_value=0.01)
            if st.form_submit_button("Log Expense"):
                u_data['expenses'].append({"Item": item, "Amount": amt})
                st.rerun()

    with col_disp:
        st.write("### Expense Tracking")
        if u_data['expenses']:
            df = pd.DataFrame(u_data['expenses'])
            total_spent = df['Amount'].sum()
            
            # --- THE ALERT SYSTEM ---
            if budget > 0:
                if total_spent > budget:
                    st.error(f"🚨 BUDGET OUTRIDDEN! You have exceeded your ${budget} limit by ${total_spent - budget:.2f}!")
                elif total_spent >= (budget * 0.8):
                    st.warning(f"⚠️ Warning: You have used {int((total_spent/budget)*100)}% of your budget.")
                else:
                    st.success(f"✅ Budget Healthy: ${budget - total_spent:.2f} remaining.")

            st.metric("Total Spent", f"${total_spent:.2f}")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No expenses logged yet. Start by adding one!")
