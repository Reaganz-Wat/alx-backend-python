import sqlite3

DB_NAME = '../python-decorators-0x01/users.db'

class DatabaseConnection():
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):  # dunder methods / magic methods
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return self.cursor
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
            self.connection.close()
            return True
        except Exception as e:
            print(f"Error: {e}")

with DatabaseConnection(DB_NAME) as cursor:
    try:
        sql_query = "SELECT * FROM users"
        cursor.execute(sql_query)
        results = cursor.fetchall()
        for id, name, email in results:
            print(f"..............................\nID: {id}\nName: {name}\nEmail: {email}")
    except Exception as e:
        print(f"Error occured: {e}")