import pandas as pd
import sqlite3

db_file = 'company.db'

conn = sqlite3.connect(db_file)

print("--- Loading the full 'employees' table ---")
query_employees = "SELECT * FROM employees;"


employee_df = pd.read_sql(query_employees, conn)
print(employee_df.head()) # .head() prints the first 5 rows

query_department_financials = pd.read_sql("SELECT * FROM department_finance", conn)
print("\n--- Department Financials Overview ---")
print(query_department_financials)
print("\n--- Loading employees with their department ID using a JOIN ---")
query_joined = """
SELECT
    e.name,
    e.department,
    d.department_id,
    e.salary
FROM
    employees AS e
LEFT JOIN
    departments AS d ON e.department = d.department
"""

joined_df = pd.read_sql(query_joined, conn)
print(joined_df.head())

print("\n--- Loading the 'revenue_generated' table ---")
revenue_df = pd.read_sql("SELECT * FROM revenue_generated", conn)
print(revenue_df)
conn.close()

print(f"\nThe average employee salary is: ${employee_df['salary'].mean():.2f}")