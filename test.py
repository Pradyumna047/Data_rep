# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 09:46:56 2025

@author: DELL
"""

# First, we need to import the pandas library, which is the most common tool for this job.
# We give it the shorter name 'pd' by convention.
import pandas as pd
import numpy as np

# --- 1. Create a "Dirty" Sample Dataset ---
# Let's imagine we have data about employees.
# This is a Python dictionary that we will turn into a table (DataFrame).
data = {
    'employee_id': [101, 102, 103, 104, 105, 102, 106, 107],
    'name': ['Alice', '  Bob', 'Charlie', 'David', 'Eve', '  Bob', 'Frank', 'Grace'],
    'department': ['Sales', 'Engineering', 'sales', 'Marketing', 'Engineering', 'Engineering', 'Finance', None],
    'salary': [70000, 80000, 65000, '90000', 82000, 80000, 75000, 85000],
    'start_date': ['2022-01-15', '2021-03-22', '2022-01-15', '2023-09-01', '2021-05-10', '2021-03-22', '2023-11-20', '2020-08-12']
}

# Create a Pandas DataFrame from our dictionary. A DataFrame is like a table.
df = pd.DataFrame(data)

print("--- 1. Original 'Dirty' Data ---")
print("Look for these issues:")
print("- Row 1 and 5 are duplicates (Bob).")
print("- 'name' column has extra spaces ('  Bob').")
print("- 'department' has inconsistent capitalization ('Sales' vs 'sales') and a missing value.")
print("- 'salary' for David is text (a string), not a number.")
print("\n")
print(df)
print("\n" + "="*40 + "\n")


# --- 2. Start the Cleansing Process ---

# --- Step 2a: Remove Duplicate Rows ---
# The drop_duplicates() method finds and removes entire rows that are identical.
# We'll keep the first instance of the duplicate row.
df_cleaned = df.drop_duplicates(keep='first')
print("--- 2a. Data After Removing Duplicates ---")
print("Bob's duplicate entry has been removed.\n")
print(df_cleaned)
print("\n" + "="*40 + "\n")


# --- Step 2b: Clean Text and Handle Inconsistent Capitalization ---
# We use the .str accessor to apply string methods to the entire column.
# .str.lower() converts all text to lowercase to make it consistent.
# .str.strip() removes any leading or trailing whitespace.
df_cleaned['name'] = df_cleaned['name'].str.strip()
#df_cleaned['department'] = df_cleaned['department'].str.lower()
df_cleaned['department'] = df_cleaned['department'].str.title()
print("--- 2b. Data After Cleaning Text ---")
print("'  Bob' is now 'Bob'.")
print("'Sales' and 'sales' are now both 'sales'.\n")
print(df_cleaned)
print("\n" + "="*40 + "\n")


# --- Step 2c: Handle Missing Data ---
# Let's find where the department is missing. A missing value is called 'NaN' (Not a Number) or 'None'.
# The fillna() method fills these missing values.
# We'll fill the missing department with 'Unassigned' to make it clear.
df_cleaned['department'] = df_cleaned['department'].fillna('Unassigned')
print("--- 2c. Data After Handling Missing Values ---")
print("The missing department is now filled with 'Unassigned'.\n")
print(df_cleaned)
print("\n" + "="*40 + "\n")


# --- Step 2d: Correct Data Types ---
# The 'salary' column contains a number stored as text. This would cause errors in calculations.
# pd.to_numeric() converts a column to a numerical type.
# errors='coerce' will turn any value that can't be converted into a number into 'NaN'.
df_cleaned['salary'] = pd.to_numeric(df_cleaned['salary'], errors='coerce')

# It's also good practice to convert date columns to a proper datetime type.
df_cleaned['start_date'] = pd.to_datetime(df_cleaned['start_date'])
print("--- 2d. Data After Correcting Data Types ---")
print("The 'salary' column is now a numeric type (float64 or int64).")
print("The 'start_date' column is now a datetime type.\n")
print(df_cleaned)
# You can check the data types with df_cleaned.info()
# print("\nFinal data types:")
# df_cleaned.info()
print("\n" + "="*40 + "\n")


# --- 3. Final Cleaned Data ---
print("--- 3. Final 'Clean' Data Ready for Analysis ---")
print("All initial issues have been addressed.\n")
print(df_cleaned)#```



### Summary of What We Cleaned:

"""| Issue | "Dirty" State | Cleaning Action | "Clean" State |
| :--- | :--- | :--- | :--- |
| **Duplicates** | Two identical rows for Bob. | `df.drop_duplicates()` | Only one row for Bob remains. |
| **Whitespace** | `'  Bob'` | `df['name'].str.strip()` | `'Bob'` |
| **Inconsistency**| `'Sales'` and `'sales'` | `df['department'].str.lower()` | Both are now `'sales'`. |
| **Missing Data** | A missing department. | `df['department'].fillna('Unassigned')` | Filled with `'Unassigned'`. |
| **Wrong Type** | Salary `'90000'` was text. | `pd.to_numeric(df['salary'])` | `90000` is now a number. |

By following this example, you can see how data cleansing is a series of logical steps to fix specific problems, making the dataset reliable for any future analysis."""