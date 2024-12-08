import mysql.connector
import pymysql
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

def connect_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            user=os.getenv("MYSQL_USER"), 
            password=os.getenv("MYSQL_PASSWORD"),
            database='ALX_prodev'
        )
        if connection:
            print("Successfully connected to MySQL server")
            return connection
    except pymysql.MySQLError as e:
        print(f"There was an error connecting to MySQL: {e}")
        return None
    
def stream_user_ages():
    connection = connect_db()
    if not connection:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row[0]  # Yield the age value
    except pymysql.MySQLError as e:
        print(f"Error fetching user ages: {e}")
    finally:
        connection.close()

def calculate_average_age():
    """
    Calculate the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age}")

if __name__ == "__main__":
    calculate_average_age()