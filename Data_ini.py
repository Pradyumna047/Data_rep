# -*- coding: utf-8 -*-
"""
Created on Sun Aug  3 09:56:43 2025

@author: DELL
"""

import pandas as pd
import numpy as np
import sqlite3 as sql3


""" Most effecient way of creating dataframe: dictionary of lists
Column-Oriented: Pandas is designed to work with data in a column-oriented fashion. Providing data as a dictionary of lists directly maps to the internal structure that pandas uses to store the DataFrame. This alignment results in a more direct and faster creation process.
Memory and Performance: This method is generally faster and more memory-efficient because pandas can directly take those lists (or even better, NumPy arrays) and construct the underlying data structures with minimal processing."""
data = {
    'employee_id': [101, 102, 103, 104, 105, 102, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116],
    'name': ['Alice', '  Bob', 'Charlie', 'David', 'Eve', '  Bob', 'Frank', 'Grace', 'Peter', 'Tony', 'Bruce', 'Chris', 'Drax', 'Steve', 'Rodey', 'Sam', 'Barton'],
    'department': ['Sales', 'Engineering', 'sales', 'Marketing', 'Engineering', 'Engineering', 'Finance', None, 'Engineering', 'sales', 'Marketing', 'Finance', 'Marketing', 'Finance', 'sales', 'Marketing', 'Finance'],
    'salary': [70000, 80000, 65000, '90000', 82000, 80000, 75000, 85000, 75000, 85000, 65000, '95000', 82000, 80000, 75000, 85000, 80000],
    'start_date': ['2022-01-15', '2021-03-22', '2022-01-15', '2023-09-01', '2021-05-10', '2021-03-22', '2023-11-20', '2020-08-12','2022-01-15', '2021-03-22', '2022-01-15', '2023-09-01', '2021-05-10', '2021-03-22', '2023-11-20', '2020-08-12', '2020-08-15']
}
df = pd.DataFrame(data)

"""efficient for performing numerical computations """
revenue = np.array([['Sales', 900000000], ['Engineering', 200000000], ['Marketing', 500000000], ['Finance', 350000000], ['HR', 100000000]])
columns = ['department', 'budget']
revenue_data = pd.DataFrame(revenue, columns=columns)

dept_data = [['Sales', 1011], ['Engineering', 1020], ['Marketing', 1015], ['Finance', 1005], ['HR', 1001]]
dept_column  = ['department', 'department_id']
department_data = pd.DataFrame(dept_data, columns=dept_column)

#file loading
df_from_excel = pd.read_excel('Revenue_generated.xlsx')

projects_data = [
    [501, 'Alpha Platform Launch', '2024-01-10', '2025-06-30', 500000],
    [502, 'Q4 Marketing Campaign', '2024-10-01', '2024-12-31', 75000]
]
projects_columns = ['project_id', 'project_name', 'start_date', 'end_date', 'budget']
df_projects = pd.DataFrame(projects_data, columns=projects_columns)

# --- Create the Employee-Project link DataFrame ---
employee_projects_data = [
    [102, 501], # Bob is on the Alpha Platform
    [105, 501], # Eve is on the Alpha Platform
    [108, 501], # Peter is on the Alpha Platform
    [104, 502], # David is on the Marketing Campaign
    [110, 502]  # Bruce is on the Marketing Campaign
]
employee_projects_columns = ['employee_id', 'project_id']
df_employee_projects = pd.DataFrame(employee_projects_data, columns=employee_projects_columns)

print("Raw data:")
print(df)

df_cleaned = df.drop_duplicates(keep='first')
df_cleaned['name'] = df_cleaned['name'].str.strip()
df_cleaned['department'] = df_cleaned['department'].str.title()
df_cleaned['department'] = df_cleaned['department'].fillna('HR')
df_cleaned['salary'] = pd.to_numeric(df_cleaned['salary'], errors='coerce')
df_cleaned['start_date'] = pd.to_datetime(df_cleaned['start_date'])

df_cleaned.to_csv('cleaned_employee_data.csv', index=False)

print("\nCleaned data has been successfully saved to 'cleaned_employee_data.csv'")

print("Cleaned data:")
print(df_cleaned)
print("Revenue data:")
print(revenue_data)
print("Department data:")
print(department_data)
print("Projects data:")
print(df_employee_projects)
print("DataFrame from a Excel file:")
print(df_from_excel)


# --- Create a database and save the tables ---

conn = sql3.connect('company.db')
# 'if_exists='replace'' will drop the table first if it already exists and create a new one. [3, 9]
# 'index=False' prevents pandas from writing the DataFrame index as a column. 
df_cleaned.to_sql('employees', conn, if_exists='replace', index=False)
revenue_data.to_sql('revenue', conn, if_exists='replace', index=False)
department_data.to_sql('departments', conn, if_exists='replace', index=False)
df_from_excel.to_sql('revenue_generated', conn, if_exists='replace', index=False)

print("\n--- Database Creation ---")
print("Database 'company.db' created and tables have been successfully saved.")

conn.close()