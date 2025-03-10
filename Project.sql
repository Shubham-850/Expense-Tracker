use expense_tracker_db
SELECT * FROM expense_tracker_db.expensetracker;


-- 1. Total amount spent per category
SELECT category, SUM(amount) AS total_spent FROM ExpenseTracker GROUP BY category;

-- 2. Total amount spent per payment mode
SELECT payment_mode, SUM(amount) AS total_spent FROM ExpenseTracker GROUP BY payment_mode;

-- 3. Total cashback received
SELECT SUM(cashback) AS total_cashback FROM ExpenseTracker;

-- 4. Top 5 most expensive categories
SELECT category, SUM(amount) AS total_spent FROM ExpenseTracker GROUP BY category ORDER BY total_spent DESC LIMIT 5;

-- 5. Spending on Transportation by payment mode
SELECT payment_mode, SUM(amount) AS total_spent FROM ExpenseTracker WHERE category = 'Transportation' GROUP BY payment_mode;

-- 6. Transactions with cashback
SELECT * FROM ExpenseTracker WHERE cashback > 0;

-- 7. Total spending per month
SELECT MONTH(date) AS month, SUM(amount) AS total_spent FROM ExpenseTracker GROUP BY MONTH(date) ORDER BY month;

-- 8. Highest spending months in Travel, Entertainment, Gifts
SELECT MONTH(date) AS month, category, SUM(amount) AS total_spent FROM ExpenseTracker WHERE category IN ('Travel', 'Entertainment', 'Gifts') GROUP BY MONTH(date), category ORDER BY total_spent DESC;

-- 9. Recurring expenses in specific months
SELECT category, MONTH(date) AS month, COUNT(*) AS occurrence_count, SUM(amount) AS total_spent FROM ExpenseTracker WHERE category IN ('Food', 'Investment', 'Groceries', 'Subscription') GROUP BY category, MONTH(date) HAVING occurrence_count > 1 ORDER BY category, month;

-- 10. Cashback earned per month
SELECT MONTH(date) AS month, SUM(cashback) AS total_cashback FROM ExpenseTracker GROUP BY MONTH(date) ORDER BY month;

-- 11. Overall spending trend over time
SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent FROM ExpenseTracker GROUP BY YEAR(date), MONTH(date) ORDER BY year, month;

-- 12. Patterns in grocery spending
SELECT DAYNAME(date) AS day_of_week, COUNT(*) AS num_transactions, SUM(amount) AS total_spent, AVG(amount) AS avg_spent FROM ExpenseTracker WHERE category = 'Groceries' GROUP BY day_of_week ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');

-- 13. High and Low Priority Categories
SELECT category, SUM(amount) AS total_spent, CASE WHEN category IN ('Groceries','Transportation','Investment', 'Bills') THEN 'High Priority' ELSE 'Low Priority' END AS priority_level FROM ExpenseTracker GROUP BY category ORDER BY priority_level DESC, total_spent DESC;

-- 14. Category with highest spending percentage
SELECT category, SUM(amount) AS total_spent, (SUM(amount) / (SELECT SUM(amount) FROM ExpenseTracker) * 100) AS percentage_of_total FROM ExpenseTracker GROUP BY category ORDER BY percentage_of_total DESC LIMIT 1;

-- 15. Total expense
SELECT SUM(amount) AS total_expense FROM ExpenseTracker;

-- 16. View full table
SELECT * FROM ExpenseTracker;

-- 17. Average spending per transaction
SELECT AVG(amount) AS avg_spent FROM ExpenseTracker;

-- 18. Most common spending category
SELECT category, COUNT(*) AS count FROM ExpenseTracker GROUP BY category ORDER BY count DESC LIMIT 1;

-- 19. Highest single transaction amount
SELECT * FROM ExpenseTracker ORDER BY amount DESC LIMIT 1;

-- 20. Months with lowest spending
SELECT MONTH(date) AS month, SUM(amount) AS total_spent FROM ExpenseTracker GROUP BY MONTH(date) ORDER BY total_spent ASC LIMIT 3;

-- 21. Percentage of transactions with cashback
SELECT (COUNT(*) / (SELECT COUNT(*) FROM ExpenseTracker) * 100) AS cashback_percentage FROM ExpenseTracker WHERE cashback > 0;

-- 22. Total transactions made
SELECT COUNT(*) AS total_transactions FROM ExpenseTracker;

-- 23. Spending trend for each category over time
SELECT category, MONTH(date) AS month, SUM(amount) AS total_spent FROM ExpenseTracker GROUP BY category, month ORDER BY category, month;

-- 24. Insert a new expense (for future data entry)
INSERT INTO ExpenseTracker (date, category, payment_mode, description, amount, cashback)
VALUES ('2025-03-11', 'Food', 'Credit Card', 'Lunch at restaurant', 20.50, 1.00);
