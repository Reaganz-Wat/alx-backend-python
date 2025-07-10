import sqlite3
from datetime import datetime

from reportlab.graphics.barcode.code128 import starta
from sympy import resultant


#### decorator to lof SQL queries
def log_queries(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        time_taken = end_time - start_time
        with open('logs.txt', 'a') as log:
            log.write(f"\n Starting... Datetime: {datetime.now()} \n{datetime.now()} | Query: {kwargs} \n Time taken: {time_taken}\n")
            print(f"{datetime.now()} | Query: {kwargs} \n Time taken: {time_taken}")
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    # results = cursor.fetchall()
    cursor.close()
    conn.close()
    return

#### fetch users while logging the query
users = fetch_all_users(query='''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL)''')