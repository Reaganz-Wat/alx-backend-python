import sqlite3


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        try:
            connection = sqlite3.connect('users.db')
            results = func(connection, *args, **kwargs)
            connection.close()
            return results
        except Exception as e:
            print(f"Error occurred: {e}")

    return wrapper

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        def wrapper(connection, *args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"Attempt {attempt}...")
                    return func(connection, *args, **kwargs)
                except Exception as e:
                    print(f"Transient error: {e}")
                    last_exception = e
                    time.sleep(delay)
            print("All retries failed.")
            raise last_exception  # re-raise last exception if all attempts fail
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)