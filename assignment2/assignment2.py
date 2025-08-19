import csv
import os
import custom_module
from datetime import datetime

# Task 2
def read_employees() -> dict:
    data = {}
    rows = []
    data.get('l')
    try:
        with open('../csv/employees.csv', newline='') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                print(row)
                if i == 0:
                    data['fields'] = row
                else:
                    rows.append(row)
        data['rows'] = rows
        return data
    except Exception as e:
        print('An exception occurred:', type(e).__name__, e)
        exit(1)

employees = read_employees()

# Task 3
def column_index(col_name) -> int:
    try:
        return employees['fields'].index(col_name)
    except ValueError:
        print(f'Column "{col_name}" not found.')
        return -1

employee_id_column = column_index('employee_id')

# Task 4
def first_name(row_num):
    idx = column_index('first_name')
    if idx == -1:
        return None
    try:
        return employees['rows'][row_num][idx]
    except (IndexError, KeyError) as e:
        print('An exception occurred:', type(e).__name__, e)
        return None

# Task 5
def employee_find(employee_id):
    idx = column_index('employee_id')
    if idx == -1:
        return []
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    return list(filter(employee_match, employees['rows']))

# Task 6
def employee_find_2(employee_id):
    return list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees['rows']))

# Task 7
def sort_by_last_name():
    idx = column_index('last_name')
    if idx == -1:
        return []
    employees['rows'].sort(key=lambda row: row[idx])
    return employees['rows']

# Task 8
def employee_dict(row):
    return {field: value for i, (field, value) in enumerate(zip(employees['fields'], row)) if i != column_index('employee_id')}

# Task 9
def all_employees_dict():
    return {row[column_index('employee_id')]: employee_dict(row) for row in employees['rows']}

# Task 10
def get_this_value():
    # os.environ['THIS_VALUE'] = 'ABC'
    return os.getenv('THIS_VALUE')

# Task 11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret('my_new_secret')

# Task 12
def read_minutes():
    def read_csv_to_dict(path):
        data = {}
        rows = []
        try:
            with open(path, newline='') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i == 0:
                        data['fields'] = row
                    else:
                        rows.append(tuple(row))
            data['rows'] = rows
            return data
        except Exception as e:
            print(f'An exception occurred while reading {path}:', type(e).__name__, e)
            exit(1)
    minutes1 = read_csv_to_dict('../csv/minutes1.csv')
    minutes2 = read_csv_to_dict('../csv/minutes2.csv')
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()

# Task 13
def create_minutes_set():
    minutes1, minutes2 = read_minutes()
    set1 = set(minutes1['rows'])
    set2 = set(minutes2['rows'])
    return set1 | set2

minutes_set = create_minutes_set()

# Task 14
def create_minutes_list():
    return list(map(lambda x: (x[0], datetime.strptime(x[1], '%B %d, %Y')), list(minutes_set)))

minutes_list = create_minutes_list()

# Task 15
def write_sorted_list():
    minutes_list.sort(key=lambda x: x[1])
    converted = list(map(lambda x: (x[0], x[1].strftime('%B %d, %Y')), minutes_list))
    try:
        with open('./minutes.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(minutes1['fields'])
            writer.writerows(converted)
    except Exception as e:
        print('An error occurred while writing minutes.csv:', type(e).__name__, e)
        exit(1)
    return converted
