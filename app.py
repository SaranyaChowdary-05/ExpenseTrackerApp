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
    if len(password) < 6: return False
    if not re.search(r"[a-z]", password): return False
    if not re.search(r"[A-Z]", password): return False
    if not re.search(r"[0-9]", password): return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password): return False
    return True

# --- 3. SESSION STATE (MOCK DATABASE) ---
# This dictionary persists as long as the tab is open.
if 'users' not in st.session_state:
    st.session_state.users = {} 
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
        st.markdown("- **Persistent Data:** Accounts stay active for your session.\n- **Budget Limits:** Set and manage your spending caps.\n- **Security:** New Forgot Password & Delete Account features.")
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
                # DATA PERSISTENCE: Saved into st.session_state.users
                st.session_state.users[u_name] = {
                    "password": p1, "name": f_name, "email": email, "budget": 0.0, "expenses": []
                }
                st.success("Account created! You can now login.")
                nav("Login")
    
    # REDIRECT TO LOGIN
    st.write("Already have an account?")
    if st.button("Go to Login"): nav("Login")
    st.button("Back to Home", on_click=lambda: nav("Home"))

# LOGIN PAGE
elif st.session_state.page == "Login":
    st.title("🔑 Secure Login")
    with st.form("login_form"):
        u_name = st.text_input("Username")
        p_word = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if u_name in st.session_state.users and st.session_state.users[u_name]["password"] == p_word:
                st.session_state.logged_in_user = u_name
                nav("Dashboard")
            else:
                st.error("Invalid credentials.")
    
    # NEW NAVIGATION FEATURES
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Forgot Password?"): nav("ForgotPassword")
    with col2:
        if st.button("New here? Register"): nav("Register")
    
    st.divider()
    st.button("Back to Home", on_click=lambda: nav("Home"))

# FORGOT PASSWORD PAGE
elif st.session_state.page == "ForgotPassword":
    st.title("🔒 Reset Password")
    st.info("Enter your username and your registered Gmail to reset your password.")
    with st.form("forgot_form"):
        u_name = st.text_input("Username")
        email = st.text_input("Registered Email")
        new_p = st.text_input("New Password", type="password")
        
        if st.form_submit_button("Update Password"):
            if u_name in st.session_state.users and st.session_state.users[u_name]["email"] == email:
                if validate_password(new_p):
                    st.session_state.users[u_name]["password"] = new_p
                    st.success("Password updated successfully!")
                    nav("Login")
                else:
                    st.error("New password does not meet security requirements.")
            else:
                st.error("Username and Email do not match our records.")
    
    if st.button("Back to Login"): nav("Login")

# DASHBOARD PAGE
elif st.session_state.page == "Dashboard":
    user = st.session_state.logged_in_user
    u_data = st.session_state.users[user]
    
    st.sidebar.title(f"Hello, {u_data['name']}")
    
    # DELETE ACCOUNT FEATURE
    if st.sidebar.button("🗑️ Delete Account", type="primary"):
        del st.session_state.users[user]
        st.session_state.logged_in_user = None
        st.warning("Account deleted.")
        nav("Home")

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
            
            if budget > 0:
                if total_spent > budget:
                    st.error(f"🚨 BUDGET EXCEEDED! Limit: ${budget} | Spent: ${total_spent}")
                elif total_spent >= (budget * 0.8):
                    st.warning(f"⚠️ Warning: {int((total_spent/budget)*100)}% used.")
                else:
                    st.success(f"✅ ${budget - total_spent:.2f} remaining.")

            st.metric("Total Spent", f"${total_spent:.2f}")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No expenses logged yet.")
