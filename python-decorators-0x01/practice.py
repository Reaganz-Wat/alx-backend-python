import sqlite3
import time

query_cache = {}

def connect_db(func):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        result = func(cursor, *args, **kwargs)
        cursor.close()
        connection.close()
        return result
    return wrapper

def cache_query(func):
    def wrapper(cursor, *args, **kwargs):

        keys = (args, tuple(sorted(kwargs.keys())))
        if keys in query_cache:
            print("Fetching from cache...")
            return query_cache[keys]
        print("Fetching Data from db...")
        result = func(cursor, *args, **kwargs)
        query_cache[keys] = result

        return result
    return wrapper

@connect_db
@cache_query
def get_user_data(cursor):
    results = cursor.execute("SELECT * FROM users").fetchall()
    return results

@connect_db
@cache_query
def get_user_by_id(cursor, id):
    results = cursor.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    return results

print(get_user_data())
time.sleep(2)
print("Cache Query: ", query_cache)
time.sleep(2)

print(get_user_data())
time.sleep(2)
print("Cache Query: ", query_cache)
time.sleep(2)

print(get_user_by_id(1))
time.sleep(2)
print("Cache Query: ", query_cache)
time.sleep(2)

print(get_user_data())
time.sleep(2)
print("Cache Query: ", query_cache)
time.sleep(2)

print(get_user_by_id(2))
time.sleep(2)
print("Cache Query: ", query_cache)
time.sleep(2)