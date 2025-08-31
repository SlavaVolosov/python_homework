#%%
import sqlite3
from sqlite3 import Cursor
import random
import pandas as pd


publisher_database = [
      'Awesome Publisher',
      'Cool Publisher',
      'Great Publisher',
      'Established Publisher',
      'Premium Publishing',
      'Elite Media Group',
    ]

magazine_database = [
        'Thick',
        'Interesting',
        'Colorful',
        'Insightful',
        'Brilliant',
        'Dynamic',
        'Creative',
        'Informative',
        'Engaging',
        'Captivating',
        'Thoughtful',
        'Inspiring',
        'Educational',
        'Entertaining',
        'Professional',
        'Innovative',
        'Spectacular',
        'Remarkable',
        'Outstanding',
        'Exceptional',
        'Comprehensive',
        'Exclusive',
        'Premium',
        'Ultimate',
        'Modern',
        'Contemporary',
        'Sophisticated',
        'Elegant',
        'Vibrant',
        'Trendy',
        'Fresh',
        'Bold',
        'Classic',
        'Timeless',
        'Progressive'
    ]

customer_database = [
    ('John Smith', '123 Oak Ave, Portland, OR, 97201'),
    ('Sarah Johnson', '456 Pine St, Seattle, WA, 98101'),
    ('Michael Brown', '789 Maple Dr, Denver, CO, 80202'),
    ('Emily Davis', '321 Elm Blvd, Austin, TX, 73301'),
    ('David Wilson', '654 Cedar Ln, Miami, FL, 33101'),
    ('Jessica Miller', '987 Birch Rd, Phoenix, AZ, 85001'),
    ('Christopher Garcia', '147 Spruce Way, Boston, MA, 02101'),
    ('Amanda Rodriguez', '258 Willow St, Chicago, IL, 60601'),
    ('Matthew Martinez', '369 Poplar Ave, Houston, TX, 77001'),
    ('Ashley Lopez', '741 Hickory Dr, Philadelphia, PA, 19101'),
    ('Daniel Anderson', '852 Chestnut Blvd, San Diego, CA, 92101'),
    ('Megan Taylor', '963 Walnut Ln, Nashville, TN, 37201'),
    ('Ryan Thomas', '159 Magnolia Rd, Atlanta, GA, 30301'),
    ('Lauren Jackson', '267 Dogwood Way, Las Vegas, NV, 89101'),
    ('Kevin White', '378 Redwood St, Minneapolis, MN, 55401'),
    ('Nicole Harris', '486 Cypress Ave, New Orleans, LA, 70112'),
    ('Brandon Martin', '591 Sycamore Dr, Kansas City, MO, 64101'),
    ('Stephanie Clark', '627 Ash Blvd, Cleveland, OH, 44101'),
    ('Justin Lewis', '738 Fir Ln, Salt Lake City, UT, 84101'),
    ('Michelle Walker', '849 Pine Ridge Rd, Richmond, VA, 23218'),
    ('Tyler Robinson', '124 Forest Ave, Tampa, FL, 33602'),
    ('Samantha Young', '235 Meadow St, Sacramento, CA, 94203'),
    ('Alexander King', '346 Valley Dr, Charlotte, NC, 28202'),
    ('Victoria Scott', '457 Ridge Blvd, Indianapolis, IN, 46201'),
    ('Nathan Green', '568 Creek Ln, Jacksonville, FL, 32202'),
    ('Rachel Adams', '679 River Rd, Columbus, OH, 43201'),
    ('Jonathan Baker', '780 Lake Ave, Detroit, MI, 48201'),
    ('Olivia Hall', '891 Park St, Memphis, TN, 38103'),
    ('Ethan Allen', '902 Garden Dr, Baltimore, MD, 21201'),
    ('Isabella Wright', '013 Harbor Blvd, Milwaukee, WI, 53201'),
    ('Jacob Nelson', '124 Beach Ln, Albuquerque, NM, 87101'),
    ('Sophia Carter', '235 Shore Rd, Tucson, AZ, 85701'),
    ('William Mitchell', '346 Bay Ave, Fresno, CA, 93701'),
    ('Emma Perez', '457 Ocean St, Mesa, AZ, 85201'),
    ('Mason Roberts', '568 Sunset Dr, Virginia Beach, VA, 23451'),
    ('Ava Turner', '679 Sunrise Blvd, Atlanta, GA, 30309'),
    ('Logan Phillips', '780 Moonlight Ln, Colorado Springs, CO, 80901'),
    ('Grace Campbell', '891 Starlight Ave, Omaha, NE, 68101'),
    ('Lucas Parker', '902 Thunder Rd, Raleigh, NC, 27601'),
    ('Chloe Evans', '013 Lightning St, Long Beach, CA, 90801')
    ]

def create_db():
    with  sqlite3.connect("../db/magazines.db") as conn:
        conn.execute("PRAGMA foreign_keys = 1") 
        cursor = conn.cursor()
    print('The database is created successfully')

def drop_all_tables():
    with  sqlite3.connect("../db/magazines.db") as conn:
        cursor = conn.cursor()
        try:
            # Create tables
            cursor.execute("""
            DROP TABLE IF EXISTS publishers
            """)

            cursor.execute("""
            DROP TABLE IF EXISTS magazines
            """)

            cursor.execute("""
            DROP TABLE IF EXISTS subscribers
            """)

            cursor.execute("""
            DROP TABLE IF EXISTS subscriptions
            """)

            conn.commit() 
            print("Tables dropped successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping all tables: {e}")

def create_tables():
    with  sqlite3.connect("../db/magazines.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers (id)
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions  (
                subscription_id INTEGER PRIMARY KEY,
                subscriber_id INTEGER,
                subscriber_name TEXT,
                magazine_id INTEGER,
                magazine_name TEXT,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers (id),
                FOREIGN KEY (magazine_id) REFERENCES magazines (id)
            )
            """)
            conn.commit() 

        except sqlite3.Error as e:
            print(f"Error creating the tables: {e}")
            
        print("Tables created successfully.")

def is_exist(cursor: Cursor, query: str, args):
    cursor.execute(query, args)
    results = cursor.fetchall()
    return len(results) > 0

def add_publisher(cursor: Cursor, name: str):
    if is_exist(
        cursor, 
        "SELECT * FROM publishers WHERE name = ?", 
        (name,)
        ):
        print(f'Publisher {name} already exists')
        return

    try:
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
        print(f'{name} is added as a publisher')
    except sqlite3.IntegrityError as e:
        print(f"Error adding {name} publisher: {e}")

def add_magazine(cursor: Cursor, name: str, publisher_name: str):
    if is_exist(
        cursor, 
        "SELECT * FROM magazines WHERE name = ?", 
        (name,)
        ):
        print(f'{name} magazine already exists')
        return

    try:
        cursor.execute("SELECT * FROM publishers WHERE name = ?", (publisher_name,))
        results = cursor.fetchall()
        if len(results) > 0:
            publisher_id = results[0][0]
        else:
            print(f"There was no publisher named {publisher_name}.")
            return

        cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
        print(f'{name} magazine published by {publisher_name} publisher is added')
    except sqlite3.IntegrityError as e:
        print(f"Error adding {name} magazine: {e}")

def add_subscriber(cursor: Cursor, name: str, address: str):
    if is_exist(
        cursor, 
        "SELECT * FROM subscribers WHERE name = ? AND address = ?", 
        (name, address)
        ):
        print(f'Subscriber {name} at address {address} already exists')
        return

    try:
        cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
        print(f'{name} is added as a subscriber')
    except sqlite3.IntegrityError as e:
        print(f"Error adding subscriber {name}: {e}")

def subscribe(cursor: Cursor, subscriber_name: str, address: str, magazine_name: str):
    cursor.execute("SELECT * FROM subscribers WHERE name = ? AND address = ?", (subscriber_name, address))
    results = cursor.fetchall()
    if len(results) > 0:
        subscriber_id = results[0][0]
    else:
        print(f"There was no subscriber named {subscriber_name}.")
        return

    cursor.execute("SELECT * FROM magazines WHERE name = ?", (magazine_name,))
    results = cursor.fetchall()
    if len(results) > 0:
        magazine_id = results[0][0]
    else:
        print(f"There was no magazine named {magazine_name}.")
        return

    if is_exist(
        cursor, 
        "SELECT * FROM subscriptions WHERE subscriber_id = ? AND magazine_id = ?", 
        (subscriber_id, magazine_id)
        ):
        print(f"Subscriber {subscriber_name} is already subscribed for {magazine_name} magazine.")
        return

    try:
        cursor.execute(
            "INSERT INTO subscriptions (subscriber_id, subscriber_name, magazine_id, magazine_name) VALUES (?, ?, ?, ?)", 
            (subscriber_id, subscriber_name, magazine_id, magazine_name))
        print(f'{subscriber_name} is subscribed for {magazine_name}')
    except sqlite3.IntegrityError as e:
        print(f"Error subscribing {subscriber_name} to {magazine_name}: {e}")

def initial_db_fillup():
    random_publisher = publisher_database[random.randint(0, len(publisher_database) - 1)]
    random_customer = customer_database[random.randint(0, len(customer_database) - 1)]
    random_magazine = magazine_database[random.randint(0, len(magazine_database) - 1)]

    with  sqlite3.connect("../db/magazines.db") as conn:
        conn.execute("PRAGMA foreign_keys = 1") 
        cursor = conn.cursor()

        for publisher in publisher_database:
            add_publisher(cursor, publisher)

        for magazine in magazine_database:
            add_magazine(
                cursor, 
                magazine, 
                publisher_database[random.randint(0, len(publisher_database) - 1)]
                )

        subscrption_options = 3
        for customer in customer_database:
            add_subscriber(cursor, *customer)
            for _ in range(random.randint(1, subscrption_options)):
                random_magazine = magazine_database[
                    random.randint(
                        0, 
                        len(magazine_database) - 1
                        )
                    ]
                subscribe(cursor, *customer, random_magazine)

        subscribe(cursor, *random_customer, random_magazine)
        add_magazine(cursor, magazine_database[1], publisher_database[3])
        subscribe(cursor, *customer_database[1], magazine_database[2])

        conn.commit()

def get_subscriber_table_list():
    with  sqlite3.connect("../db/magazines.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscribers")
        results = cursor.fetchall()
        return [result for result in results]

def get_subscriber_table_df():
    with  sqlite3.connect("../db/magazines.db") as conn:
        return pd.read_sql_query('SELECT * FROM subscribers', conn)

def get_sorted_magazines_df():
    with  sqlite3.connect("../db/magazines.db") as conn:
        return pd.read_sql_query('SELECT * FROM magazines', conn).sort_values(by='name')

def get_publishers_magazines_df(publisher_name: str):
    with  sqlite3.connect("../db/magazines.db") as conn:
        return pd.read_sql_query(
            f"""
            SELECT m.name FROM magazines m
            JOIN publishers p
            ON m.publisher_id = p.id
            WHERE p.name = '{publisher_name}'
            """, 
            conn
            )

#%% Task 1: Create a New SQLite Database
create_db()

#%% Task 2: Define Database Structure
create_tables()

#%% Task 3: Populate Tables with Data
initial_db_fillup()

#%% Task 4: Write SQL Queries
lst = get_subscriber_table_list()

df = get_subscriber_table_df()
print(df)
df = get_sorted_magazines_df()
print(df)
lst = get_publishers_magazines_df('Premium Publishing')
print(lst)

#%%
drop_all_tables()

# %%
