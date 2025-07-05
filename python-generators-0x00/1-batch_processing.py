import seed

def stream_users_in_batches(batch_size=10):
    """
    Generator that yields batches of rows from the user_data table
    """
    connection = seed.connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        columns = [desc[0] for desc in cursor.description]

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            # yield one full batch at a time
            yield [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Error during batch fetch: {e}")
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size=10):
    """
    Generator that filters users with age > 25 from each batch
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                yield user
