import seed

def stream_users():
    connection = seed.connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        columns = [desc[0] for desc in cursor.description]

        for row in cursor:
            yield dict(zip(columns, row))
    except Exception as e:
        print(f"Error streaming users: {e}")
    finally:
        cursor.close()
        connection.close()