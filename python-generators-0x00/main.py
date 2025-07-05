from itertools import islice

seed = __import__('seed')
stream_users = __import__('0-stream_users')
processing = __import__('1-batch_processing')
lazy_paginator = __import__('2-lazy_paginate').lazy_pagination
cal_avg = __import__('4-stream_ages').calculate_average_age

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

def batch_processing():
    for batch in processing.stream_users_in_batches(10):
        print(batch)

def filter_ages():
    for batch in processing.batch_processing(10):
        print(batch)

def lazy_pagination():
    for page in lazy_paginator(10):
        for user in page:
            print(user)

if __name__ == "__main__":
    # main()
    # stream_data()
    # batch_processing()
    # filter_ages()
    # lazy_pagination()
    cal_avg()