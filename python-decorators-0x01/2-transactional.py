import sqlite3
import functools

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        global results
        try:
            connection = sqlite3.connect("users.db")
            results = func(connection, *args, **kwargs)
        except Exception as e:
            print(f"Error occured: {e}")

        return results
    return wrapper

def transactional(func):
    """This calls the function to make changes into the database, and then commits if there is no error, else it doesnt"""
    def wrapper(connection, *args, **kwargs):
        results = None
        try:
            results = func(connection, *args, **kwargs)
            print("Commiting...")
            connection.commit()
        except Exception as e:
            print(f"Got an error: {e}")
            print(f"Rolling back...")
            connection.rollback()
        return results
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    #### Update user's email with automatic transaction handling

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')