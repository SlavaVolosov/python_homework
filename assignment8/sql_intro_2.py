#%%
import pandas as pd
import sqlite3


def get_df():
    with sqlite3.connect("../db/lesson.db") as conn:
        sql_statement = """
        SELECT line_item_id, product_name, quantity, l.product_id, price FROM line_items l 
        JOIN products p 
        ON l.product_id = p.product_id ;
        """
        return pd.read_sql_query(sql_statement, conn)

#%% Task 5: Read Data into a DataFrame
df = get_df()
print(df.head())

#%%
df['total'] = df['quantity'] * df['price']
print(df.head())

#%%
grouped_df = df.groupby('product_id').agg({'product_name': 'first', 'line_item_id': 'count', 'total': 'sum'})
print(grouped_df.head())

#%%
sorted_df = grouped_df.sort_values(by='product_name')
print(sorted_df.head())

#%%
sorted_df.to_csv('order_summary.csv', index=False)

# %%
