import pymysql
import csv
import uuid
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

def connect_db():
    try:
        print(f"Connecting to MySQL server with user: {os.getenv('MYSQL_USER')}")
        connection = pymysql.connect(
            host='localhost',
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD")
        )
        print("Successfully connected to MySQL server")
        return connection
    except pymysql.MySQLError as e:
        print(f"There was an error connecting to MySQL: {e}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Successfully created ALX_prodev.")
    except pymysql.MySQLError as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    try:
        connection = pymysql.connect(
            host='localhost',
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database='ALX_prodev'
        )
        print("Successfully connected to ALX_prodev database")
        return connection
    except pymysql.MySQLError as e:
        print(f"There was an error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age DECIMAL(3,0) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print("Successfully created user_data table.")
    except pymysql.MySQLError as e:
        print(f"There was an error creating table: {e}")

def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        for row in data:
            try:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
            except pymysql.MySQLError as e:
                print(f"Error inserting data: {e}")
        connection.commit()
        print("Successfully inserted data.")
    except pymysql.MySQLError as e:
        print(f"There was an error inserting data: {e}")

def load_csv_data(filepath):
    try:
        with open(filepath, mode='r') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
        return data
    except Exception as e:
        print(f"There was an error loading CSV data: {e}")
        return []

if __name__ == "__main__":
    csv_file = 'user_data.csv'

    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

    prodev_connection = connect_to_prodev()
    if prodev_connection:
        create_table(prodev_connection)
        user_data = load_csv_data(csv_file)
        if user_data:
            insert_data(prodev_connection, user_data)

        prodev_connection.close()
