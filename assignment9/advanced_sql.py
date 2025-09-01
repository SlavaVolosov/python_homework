#%%
import pandas as pd
import numpy as np
import sqlite3
import os


#%% Task 1: Complex JOINs with Aggregation
with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = """
    SELECT o.order_id, COUNT(*) as item_count, SUM(l.quantity * p.price) as total_value
    FROM orders o 
    JOIN line_items l ON o.order_id = l.order_id
    JOIN products p ON p.product_id = l.product_id 
    GROUP BY o.order_id
    LIMIT 5
    """
    df = pd.read_sql_query(sql_statement, conn)
    print(df)

#%% Task 2: Understanding Subqueries
with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = """
    SELECT c.customer_id, c.customer_name, AVG(total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id, o.order_id, l.product_id, l.quantity, p.price, SUM(l.quantity * p.price) AS total_price
        FROM orders o 
        JOIN line_items l ON o.order_id = l.order_id
        JOIN products p ON p.product_id = l.product_id 
        GROUP BY o.order_id
        ORDER BY customer_id
    ) AS subq
    ON c.customer_id = subq.customer_id
    GROUP BY c.customer_id
    ORDER BY c.customer_id
    --LIMIT 35
    """
    df = pd.read_sql_query(sql_statement, conn)
    print(df)

#%% Task 3: An Insert Transaction Based on Data
print(f"Database file exists: {os.path.exists('../db/lesson.db')}")
print(f"Database file permissions: {oct(os.stat('../db/lesson.db').st_mode)}")

def insert_order():
    find_customer_sql = '''
    SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'
    '''
    find_employee_sql = '''
    SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'
    '''
    insert_order_sql = '''
    INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, JULIANDAY('now')) RETURNING order_id
    '''
    with sqlite3.connect("../db/lesson.db") as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        cursor.execute(find_customer_sql)
        customer_id = cursor.fetchone()[0]

        cursor.execute(find_employee_sql)
        employee_id = cursor.fetchone()[0]

        try:
            cursor.execute(insert_order_sql, (customer_id, employee_id))
            order_id = cursor.fetchone()[0]
            conn.commit()
            return order_id

        except sqlite3.IntegrityError as e:
            print(f"Data constraint error: {e}")
            conn.rollback()
        except sqlite3.OperationalError as e:
            print(f"Database operation error: {e}")
            conn.rollback()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
        return None


def insert_line_items(order_id: int):
    find_product_sql = '''
    SELECT * FROM products ORDER BY price ASC LIMIT 5
    '''
    insert_line_item_sql = '''
    INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?) RETURNING line_item_id
    '''
    product_quantity = 10
    li_id_list_db = []
    with sqlite3.connect("../db/lesson.db") as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        try:
            cursor.execute(find_product_sql)
            product_list = cursor.fetchall()
            for product in product_list:
                product_id, product_name, price = product
                cursor.execute(insert_line_item_sql, (order_id, product_id, product_quantity))
                line_item_id = cursor.fetchone()[0]
                li_id_list_db.append(line_item_id)
            conn.commit()
            return li_id_list_db
        except sqlite3.IntegrityError as e:
            print(f"Data constraint error: {e}")
            conn.rollback()
        except sqlite3.OperationalError as e:
            print(f"Database operation error: {e}")
            conn.rollback()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
        return None

def get_li_id_list(order_id: int):
    with sqlite3.connect("../db/lesson.db") as conn:
        sql_statement = f"""
        SELECT line_item_id, l.product_id, p.product_name, quantity
        FROM line_items l
        JOIN products p
        ON l.product_id = p.product_id
        WHERE l.order_id = {order_id}
        """
        df = pd.read_sql_query(sql_statement, conn)
    return df['line_item_id'].to_list()

order_id = insert_order()
if order_id:
    li_id_list_db = insert_line_items(order_id)
    li_id_list_sql  =get_li_id_list(order_id)
    is_valid = np.array_equal(set(li_id_list_db), set(li_id_list_sql))
    print(f'Check for validity. Valid: {is_valid}')

#%% Task 4: Aggregation with HAVING
with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = f"""
    SELECT first_name, last_name, COUNT(o.order_id) AS order_count
    FROM employees e
    JOIN orders o
    ON e.employee_id = o.employee_id
    GROUP BY e.employee_id
    HAVING order_count > 5
    ORDER BY order_count desc
    """
    df = pd.read_sql_query(sql_statement, conn)
    print(df)
