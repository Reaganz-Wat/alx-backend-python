import seed

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT age FROM user_data")
        while True:
            row = cursor.fetchone()
            if not row:
                break
            yield row[0]  # extract the age value
    except Exception as e:
        print("Error fetching ages:", e)
    finally:
        cursor.close()
        connection.close()


def calculate_average_age():
    """
    Calculates average age using the stream_user_ages generator
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += float(age)  # convert to float in case it's decimal
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")
