from itertools import islice

seed = __import__('seed')
stream_users = __import__('0-stream_users')

def main():
    connection = seed.connect_db()
    if connection:
        seed.create_database(connection)
        connection.close()
        print("Connection to default DB successful")

        connection = seed.connect_to_prodev()
        if connection:
            seed.create_table(connection)
            seed.insert_data(connection, 'user_data.csv')

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_data LIMIT 5;")
            rows = cursor.fetchall()
            print("Sample rows from user_data:")
            for row in rows:
                print(row)
            cursor.close()

def stream_data():
    for x in islice(stream_users.stream_users(), 6):
        print(x)


if __name__ == "__main__":
    # main()
    stream_data()