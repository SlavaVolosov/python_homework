import csv
from pprint import pprint

# Task 3
def read_employees() -> dict:
    rows = []
    try:
        with open('csv/employees.csv', newline='') as file:
            rows = [row for row in csv.reader(file)][1:]
        return rows
    except Exception as e:
        print('An exception occurred:', type(e).__name__, e)
        exit(1)

employees = read_employees()
pprint(employees)

employee_names = [f'{row[1]} {row[2]}' for row in employees]
pprint(employee_names)

employee_names_containing_e = [f'{row[1]} {row[2]}' for row in employees if 'e' in row[1] or 'e' in row[2]]
pprint(employee_names_containing_e)
