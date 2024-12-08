import mysql.connector
import pymysql
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values
import os
from datetime import datetime
from time import sleep

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
    
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed with error: {e}")
                    if attempts < retries:
                        print(f"Retrying in {delay} seconds...")
                        sleep(delay)
                    else:
                        print("Max retries reached. Operation failed.")
                        raise
        return wrapper
    return decorator

@retry_on_failure(retries=3, delay=2)
def insert_user(connection, user_id, name, email, age):
    cursor = connection.cursor()
    query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, name, email, age))
    connection.commit()
    print(f"User {name} inserted successfully.")

if __name__ == "__main__":
    connection = connect_db()
    if connection:
        try:
            insert_user(connection, "123e4567-e89b-12d3-a456-426614174003", "John Doe", "john.doe@example.com", 30)
        finally:
            connection.close()