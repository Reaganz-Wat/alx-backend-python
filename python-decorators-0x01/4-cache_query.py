import sqlite3

# Global cache
query_cache = {}

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        try:
            conn = sqlite3.connect('users.db')
            result = func(conn, *args, **kwargs)
            conn.close()
            return result
        except Exception as e:
            print(f"Error occurred: {e}")
    return wrapper

def cache_query(func):
    def wrapper(conn, *args, **kwargs):
        # Extract the query argument (positional or keyword)
        query = kwargs.get("query") or (args[0] if args else None)

        if query in query_cache:
            print("📦 Using cached result for query")
            return query_cache[query]
        else:
            print("🔄 Executing and caching query")
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — should hit DB and cache result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call — should use cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
