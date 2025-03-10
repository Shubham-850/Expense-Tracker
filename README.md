# Expense-Tracker
A Streamlit-based Expense Tracker Dashboard that retrieves and visualizes personal expenses from a MySQL database. Features include spending analysis, cashback tracking, interactive visualizations, and data insertion. Built with Python, Streamlit, Pandas, Plotly, and MySQL.


# Expense Tracker Dashboard

## Overview
The Expense Tracker Dashboard is a Streamlit-based web application that helps users analyze and visualize their personal expenses. The app retrieves expense data from a MySQL database and provides various insights through SQL queries and interactive visualizations.

## Features
- View total spending by category and payment mode
- Identify top spending categories
- Analyze spending trends over time
- Track cashback rewards
- Identify recurring expenses
- View full expense table with adjustable row selection
- Insert new expense records via the UI
- Visualizations using Plotly for better insights

## Technologies Used
- Python
- Streamlit
- MySQL
- Pandas
- Plotly
- Faker (for generating synthetic data)

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python installed and then install required libraries:
```bash
pip install streamlit pandas mysql-connector-python plotly faker
```

### 2. Setup MySQL Database
Create a database and table in MySQL:
```sql
CREATE DATABASE expense_tracker_db;
USE expense_tracker_db;

CREATE TABLE ExpenseTracker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(255) NOT NULL,
    payment_mode VARCHAR(255) NOT NULL,
    description TEXT,
    amount DECIMAL(10,2) NOT NULL,
    cashback DECIMAL(10,2) DEFAULT 0
);
```

### 3. Run the Streamlit App
Start the Streamlit application:
```bash
streamlit run app.py
```

## Version Control
Track progress using Git and push changes to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Future Enhancements
- Implement user authentication
- Add export to CSV feature
- Introduce advanced filtering options

