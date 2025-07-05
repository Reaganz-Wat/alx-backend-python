import csv
import uuid
import psycopg2
from dotenv import load_dotenv
import os

from matplotlib.backend_bases import cursors

"""Loads environment variables from .env file"""
load_dotenv()

# Database connection details
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT"))

def connect_db():
    """Connects to database server"""

    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def create_database(connection):
    """Creates the database if it does not exist"""
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"Database {DB_NAME} created")
        else:
            print(f"Database {DB_NAME} already exists")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        connection.autocommit = False


def connect_to_prodev():
    """Connects the ALX_prodev database in MYSQL"""

    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def create_table(connection):
    """Creates the user_data table"""
    cursor = connection.cursor()
    query = """
       CREATE TABLE IF NOT EXISTS user_data (
           user_id UUID PRIMARY KEY,
           name VARCHAR NOT NULL,
           email VARCHAR NOT NULL,
           age DECIMAL NOT NULL
       );
       """
    try:
        cursor.execute(query)
        connection.commit()
        print("Table user_data created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")
        connection.rollback()
    finally:
        cursor.close()

def insert_data(connection, csv_file_path):
    """Insert data from CSV and generate user_id"""
    cursor = connection.cursor()
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()