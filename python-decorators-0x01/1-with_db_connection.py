import sqlite3
import functools

def with_db_connection(func):
    """ your code goes here"""
    def wrapper(*args, **kwargs):

        connection = sqlite3.connect('users.db')

        results = func(connection, *args, **kwargs)

        connection.close()

        return results

    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
    #### Fetch user by ID with automatic connection handling

user = get_user_by_id(user_id=1)
print(user)