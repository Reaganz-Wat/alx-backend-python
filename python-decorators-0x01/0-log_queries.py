import sqlite3

#### decorator to lof SQL queries
def log_queries(func):
    def wrapper(*args, **kwargs):
        print(f"The Query is: {kwargs}")

        return func(*args, **kwargs)

        print("Finished running querry")

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