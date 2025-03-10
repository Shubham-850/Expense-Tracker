import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# Function to connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="expense_tracker_db"
    )

# Function to fetch data from the database
def fetch_query(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to insert new expense data
def insert_expense(date, category, payment_mode, description, amount, cashback):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO ExpenseTracker (date, category, payment_mode, description, amount, cashback)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (date, category, payment_mode, description, amount, cashback))
    conn.commit()
    cursor.close()
    conn.close()

# Streamlit UI setup
st.title("Expense Tracker Dashboard")
st.header("Visualizing Expense Insights")

# Dictionary of SQL queries
queries = {
    "View full table": "SELECT * FROM ExpenseTracker;",
    "Total amount spent per category": "SELECT category, SUM(amount) as total_spent FROM ExpenseTracker GROUP BY category;",
    "Total amount spent per payment mode": "SELECT payment_mode, SUM(amount) as total_spent FROM ExpenseTracker GROUP BY payment_mode;",
    "Total cashback received": "SELECT SUM(cashback) as total_cashback FROM ExpenseTracker;",
    "Top 5 most expensive categories": "SELECT category, SUM(amount) as total_spent FROM ExpenseTracker GROUP BY category ORDER BY total_spent DESC LIMIT 5;",
    "Spending on Transportation by payment mode": "SELECT payment_mode, SUM(amount) as total_spent FROM ExpenseTracker WHERE category = 'Transportation' GROUP BY payment_mode;",
    "Transactions with cashback": "SELECT * FROM ExpenseTracker WHERE cashback > 0;",
    "Total spending per month": "SELECT MONTH(date) as month, SUM(amount) as total_spent FROM ExpenseTracker GROUP BY MONTH(date) ORDER BY month;",
    "Highest spending months in Travel, Entertainment, Gifts": "SELECT MONTH(date) as month, category, SUM(amount) as total_spent FROM ExpenseTracker WHERE category IN ('Travel', 'Entertainment', 'Gifts') GROUP BY MONTH(date), category ORDER BY total_spent DESC;",
    "Recurring expenses in specific months": "SELECT category, MONTH(date) as month, COUNT(*) as occurrence_count, SUM(amount) as total_spent FROM ExpenseTracker WHERE category IN ('Food', 'investment', 'Groceries', 'Subscription') GROUP BY category, MONTH(date) HAVING occurrence_count > 1 ORDER BY category, month;",
    "Cashback earned per month": "SELECT MONTH(date) AS month, SUM(cashback) AS total_cashback FROM ExpenseTracker GROUP BY MONTH(date) ORDER BY month;",
    "Overall spending trend over time": "SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent FROM ExpenseTracker GROUP BY YEAR(date), MONTH(date) ORDER BY year, month;",
    "Patterns in grocery spending": "SELECT DAYNAME(date) as day_of_week, COUNT(*) as num_transactions, SUM(amount) as total_spent, AVG(amount) as avg_spent FROM ExpenseTracker WHERE category = 'Groceries' GROUP BY day_of_week ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');",
    "High and Low Priority Categories": "SELECT category, SUM(amount) as total_spent, CASE WHEN category IN ('Groceries','Transportation','investment', 'bills') THEN 'High Priority' ELSE 'Low Priority' END as priority_level FROM ExpenseTracker GROUP BY category ORDER BY priority_level DESC, total_spent DESC;",
    "Category with highest spending percentage": "SELECT category, SUM(amount) as total_spent, (SUM(amount) / (SELECT SUM(amount) FROM ExpenseTracker) * 100) as percentage_of_total FROM ExpenseTracker GROUP BY category ORDER BY percentage_of_total DESC LIMIT 1;",
    "Total expense": "SELECT SUM(amount) as total_expense FROM ExpenseTracker;",   
    "Average spending per transaction": "SELECT AVG(amount) as avg_spent FROM ExpenseTracker;",
    "Most common spending category": "SELECT category, COUNT(*) as count FROM ExpenseTracker GROUP BY category ORDER BY count DESC LIMIT 1;",
    "Highest single transaction amount": "SELECT * FROM ExpenseTracker ORDER BY amount DESC LIMIT 1;",
    "Months with lowest spending": "SELECT MONTH(date) as month, SUM(amount) as total_spent FROM ExpenseTracker GROUP BY MONTH(date) ORDER BY total_spent ASC LIMIT 3;",
    "Percentage of transactions with cashback": "SELECT (COUNT(*) / (SELECT COUNT(*) FROM ExpenseTracker) * 100) as cashback_percentage FROM ExpenseTracker WHERE cashback > 0;",
    "Total transactions made": "SELECT COUNT(*) as total_transactions FROM ExpenseTracker;",
    "Spending trend for each category over time": "SELECT category, MONTH(date) as month, SUM(amount) as total_spent FROM ExpenseTracker GROUP BY category, month ORDER BY category, month;"
}

# Sidebar selection
query_name = st.sidebar.selectbox("Select an insight to display", list(queries.keys()))

# Execute query
if query_name:
    data = fetch_query(queries[query_name])
    st.subheader(query_name)
    
    if query_name == "View full table":
        num_rows = st.slider("Select number of rows to display", min_value=5, max_value=len(data), value=10)
        st.write(data.head(num_rows))
    else:
        st.write(data)
    
    # Visualization
    if "category" in data.columns and "total_spent" in data.columns:
        fig = px.bar(data, x="category", y="total_spent", title=query_name, color="total_spent")
        st.plotly_chart(fig)
    elif "payment_mode" in data.columns and "total_spent" in data.columns:
        fig = px.pie(data, names="payment_mode", values="total_spent", title=query_name)
        st.plotly_chart(fig)
    elif "month" in data.columns and "total_spent" in data.columns:
        fig = px.line(data, x="month", y="total_spent", title=query_name, markers=True)
        st.plotly_chart(fig)
    elif "day_of_week" in data.columns and "total_spent" in data.columns:
        fig = px.bar(data, x="day_of_week", y="total_spent", title=query_name, color="total_spent")
        st.plotly_chart(fig)

# Form to insert new expenses
st.sidebar.header("Add a New Expense")
date = st.sidebar.date_input("Date")
category = st.sidebar.text_input("Category")
payment_mode = st.sidebar.text_input("Payment Mode")
description = st.sidebar.text_area("Description")
amount = st.sidebar.number_input("Amount", min_value=0.01, format="%.2f")
cashback = st.sidebar.number_input("Cashback", min_value=0.00, format="%.2f")

if st.sidebar.button("Add Expense"):
    insert_expense(date, category, payment_mode, description, amount, cashback)
    st.sidebar.success("Expense added successfully!")
