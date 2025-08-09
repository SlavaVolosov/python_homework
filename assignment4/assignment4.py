# %%
import pandas as pd
from datetime import datetime

# Task 1
my_dict = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
salary = [70000, 80000, 90000]

task1_data_frame = pd.DataFrame(my_dict)

task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = pd.Series(salary)
task1_older = task1_with_salary.copy()
task1_older['Age'] += 1

task1_older.to_csv('employees.csv', index=False)

# Task 2
task2_employees = pd.read_csv('employees.csv')

json_employees = pd.read_json('additional_employees.json')
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)

# Task 3
first_three = more_employees.head(3)

last_two = more_employees.tail(2)

employee_shape = more_employees.shape
print(f'Number of rows: {employee_shape[0]}, Number of columns: {employee_shape[1]}')

print(more_employees.info())

# Task 4
dirty_data = pd.read_csv('dirty_data.csv')

clean_data = dirty_data.copy().drop_duplicates()

clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
mean_age = clean_data['Age'].mean()
clean_data['Age'] = clean_data['Age'].fillna(mean_age).astype(int)

clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')
mean_salary = clean_data['Salary'].median()
clean_data['Salary'] = clean_data['Salary'].fillna(mean_salary).astype(int)

clean_data['Hire Date'] = clean_data['Hire Date'].str.strip().str.replace('-', '/')
# added a custom lambda to get rid of one last NaT
clean_data['Hire Date'] = clean_data['Hire Date'].map(
    lambda x: datetime.strptime(x, '%m/%d/%Y') if '/' in x[:3] else x
)
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], errors='coerce')

clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()

# %%
