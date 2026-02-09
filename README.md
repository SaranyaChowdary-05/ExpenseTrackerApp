# 💰 Expense Tracker – Smart Expense Management System

Expense Tracker is a Streamlit-based personal finance management web application that helps users track expenses, manage monthly budgets, and receive intelligent alerts when spending limits are close to or exceeded.

This project demonstrates session-based authentication, expense tracking, budget monitoring, and basic AI/ML foundations using Python.

---

## 🚀 Features

### 🔐 Authentication & Security
- User Registration and Login
- Gmail-only email validation
- Strong password enforcement:
  - Minimum 6 characters
  - Uppercase, lowercase, number, and special character
- Forgot Password functionality
- Delete Account option
- Session-based mock database (no external database required)

### 💸 Expense Management
- Add and track daily expenses
- Real-time calculation of total expenses
- Expense history displayed in tabular format

### 💰 Budget Control
- Set monthly budget limits
- Smart alerts:
  - ✅ Safe zone
  - ⚠️ 80% budget warning
  - 🚨 Budget exceeded alert

### 📊 Dashboard
- Interactive and responsive Streamlit UI
- Sidebar navigation
- Live metrics and alerts for better financial awareness

---

## 🧠 AI / ML Component
- Uses Linear Regression as a foundation (scikit-learn)
- Designed for future enhancements such as:
  - Expense prediction
  - Spending trend analysis
  - Budget recommendations

---

## 🛠️ Tech Stack

- Frontend & Backend: Streamlit
- Programming Language: Python
- Libraries Used:
  - streamlit
  - pandas
  - numpy
  - scikit-learn
  - re (Regular Expressions)

---

## 📂 Project Structure

Expense-Tracker/
│
├── app.py          # Main Streamlit application
├── README.md       # Project documentation
└── requirements.txt

---

## 📦 Installation & Setup

### 1. Clone the Repository
git clone https://github.com/your-username/Expense-Tracker.git  
cd Expense-Tracker

### 2. Install Dependencies
pip install streamlit pandas numpy scikit-learn

### 3. Run the Application
streamlit run app.py

The application will open automatically in your browser.

---

## 🧪 How to Use

1. Register with a valid Gmail address
2. Create a strong password
3. Login to access the dashboard
4. Set your monthly budget
5. Add expenses
6. Monitor alerts and remaining balance
7. Logout or delete your account anytime

---

## ⚠️ Important Notes

- Data is stored using Streamlit Session State
- Data persists only while the browser tab remains open
- No external APIs or API keys are required
- Ideal for academic and prototype-level projects

---

## 🎯 Future Enhancements

- Database integration (SQLite / MongoDB)
- Expense prediction graphs
- Category-wise spending analysis
- Export expense reports (CSV / PDF)
- Deployment on Streamlit Cloud

---

## 👩‍💻 Author

Saranya G  
AI / ML Enthusiast  
Project: Expense Tracker

---

## 📜 License

This project is intended for educational purposes only.
