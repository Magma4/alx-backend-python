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


def stream_users():
    connection = connect_db()
    if not connection:
        print("Could not connect to the database.")
        return

    try:
        # Use DictCursor to fetch rows as dictionaries
        user_data = connection.cursor(cursor=pymysql.cursors.DictCursor)
        user_data.execute("SELECT * FROM user_data")

        for row in user_data:  # Iterate over the result
            yield row

    except pymysql.MySQLError as e:
        print(f"There was an error fetching data: {e}")
    finally:
        connection.close()

# Test the generator
if __name__ == "__main__":
    user_stream = stream_users()
    print(next(user_stream))  # Print the first user