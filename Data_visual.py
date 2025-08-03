# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 14:04:01 2025

@author: DELL
"""


import pandas as pd
import sqlite3 as sql3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

conn = sql3.connect('company.db')

query = """
    SELECT
        e.employee_id,
        e.name,
        e.department,
        e.salary,
        e.start_date,
        d.department_id,
        r.revenue_generated
    FROM
        employees e
    LEFT JOIN
        departments d ON e.department = d.department
    LEFT JOIN
        revenue_generated r ON e.employee_id = r.employee_id;
    """
df_analysis = pd.read_sql(query, conn)

df_revenue_budget = pd.read_sql("SELECT * FROM revenue", conn)

# Ensure numeric columns from the database are treated as numbers
df_analysis['salary'] = pd.to_numeric(df_analysis['salary'], errors='coerce')
df_revenue_budget['budget'] = pd.to_numeric(df_revenue_budget['budget'], errors='coerce')
df_analysis['revenue_generated'] = pd.to_numeric(df_analysis['revenue_generated'], errors='coerce')
df_analysis['start_date'] = pd.to_datetime(df_analysis['start_date'])


total_salary_per_dept = df_analysis.groupby('department')['salary'].sum().reset_index()
total_salary_per_dept.rename(columns={'salary': 'total_salary_cost'}, inplace=True)

df_dept_financials = pd.merge(df_revenue_budget, total_salary_per_dept, on='department')

df_dept_financials['salary_as_pct_of_budget'] = \
    (df_dept_financials['total_salary_cost'] / df_dept_financials['budget']) * 100

df_dept_financials['remaining_budget'] = \
    df_dept_financials['budget'] - df_dept_financials['total_salary_cost']

print("\nDepartment Financials Overview:")
print(df_dept_financials)
df_dept_financials.to_sql('department_finance', conn, if_exists='replace', index=False)

avg_revenue_per_dept = df_analysis.groupby('department')['revenue_generated'].mean().sort_values(ascending=False)
print("\nAverage Revenue Generated per Employee in Each Department:")
print(avg_revenue_per_dept)

sns.set_style("whitegrid")

df_dept_financials.plot(
    x='department',
    y=['budget', 'total_salary_cost'],
    kind='bar',
    figsize=(12, 7),
    title='Department Budget vs. Total Salary Cost'
)
plt.ylabel('Amount ($)')
plt.xlabel('Department')
plt.xticks(rotation=45, ha='right')
plt.title('Department Budget vs. Total Salary Cost', fontsize=16)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 7))
sns.barplot(x='department', y='salary_as_pct_of_budget', data=df_dept_financials.sort_values('salary_as_pct_of_budget', ascending=False), palette='coolwarm')
plt.title('Salary Cost as a Percentage of Department Budget', fontsize=16)
plt.ylabel('Percentage of Budget (%)')
plt.xlabel('Department')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
avg_revenue_per_dept.plot(kind='bar', color=sns.color_palette('magma'))
plt.title('Average Revenue Generated per Employee by Department', fontsize=16)
plt.ylabel('Average Revenue ($)')
plt.xlabel('Department')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='salary',
    y='revenue_generated',
    hue='department',  # Color points by department
    size='revenue_generated', # Make points bigger for higher revenue
    sizes=(50, 500),
    alpha=0.7,
    data=df_analysis
)
plt.title('Employee Salary vs. Revenue Generated', fontsize=16)
plt.xlabel('Salary ($)')
plt.ylabel('Revenue Generated ($)')
plt.legend(title='Department')
plt.grid(True)
plt.show()

conn.close()
