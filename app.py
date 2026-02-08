import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Setup
st.set_page_config(page_title="SpendWise AI", layout="wide")

# 2. AI Model & Data
@st.cache_data
def load_data_and_predict():
    # Synthetic dataset for training
    days = np.arange(1, 31).reshape(-1, 1)
    spending = 20 + (days.flatten() * 1.5) + np.random.normal(0, 5, 30)
    df = pd.DataFrame({'Day': days.flatten(), 'Amount': spending})
    
    # Train Linear Regression Model
    model = LinearRegression()
    model.fit(days, spending)
    prediction = model.predict([[31]])[0]
    return df, prediction

df, forecast = load_data_and_predict()

# 3. Navigation Logic
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# 4. Home Page
if st.session_state.page == 'Home':
    st.title("🚀 SpendWise AI")
    st.subheader("Smart Finance Tracking & Predictive Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### AI-Powered Budgeting")
        st.markdown("- **Forecasts:** Predicts next month's bills.")
        st.markdown("- **Insights:** Visualizes spending trends.")
        if st.button("Login to Dashboard", use_container_width=True):
            st.session_state.page = 'Dashboard'
            st.rerun()
    with col2:
        st.image("https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&q=80&w=800")

# 5. Dashboard Page
else:
    st.title("📊 AI Expense Dashboard")
    if st.sidebar.button("Logout"):
        st.session_state.page = 'Home'
        st.rerun()
        
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Spent", f"${df['Amount'].sum():.2f}")
    m2.metric("Daily Avg", f"${df['Amount'].mean():.2f}")
    m3.metric("AI Forecast (Tomorrow)", f"${forecast:.2f}")

    st.divider()
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Add Expense")
        with st.form("entry"):
            st.text_input("Item")
            st.number_input("Cost", min_value=0.0)
            if st.form_submit_button("Log Expense"):
                st.success("Transaction Logged!")
    with c2:
        st.subheader("Spending Pattern")
        st.line_chart(df.set_index('Day'))
