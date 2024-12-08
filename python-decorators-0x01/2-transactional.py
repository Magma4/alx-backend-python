import mysql.connector
import pymysql
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values
import os
from datetime import datetime

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
    
def with_db_connection(func):
    def wrapper(*args, **kwargs):
        connection = connect_db()
        if not connection:
            print("Failed to connect to the database.")
            return
        try:
            result = func(connection, *args, **kwargs)
        finally:
            connection.close()
            print("Database connection closed.")
        return result
    return wrapper

def transactional(func):
    def wrapper(connection, *args, **kwargs):
        try:
            result = func(connection, *args, **kwargs) 
            connection.commit()
            print("Transaction committed successfully.")
            return result
        except Exception as e:
            connection.rollback() 
            print(f"Transaction has been rolled back due to error: {e}")
            raise 
    return wrapper

@with_db_connection
@transactional
def insert_user(connection, user_id, name, email, age):
    cursor = connection.cursor()
    query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, name, email, age))
    print(f"User {name} inserted successfully.")

if __name__ == "__main__":
    try:
        insert_user("123e4567-e89b-12d3-a456-426614175112", "Raymond Frimpong", "raymond.frimpong@gmail.com", 29)
    except Exception as e:
        print(f"Error inserting user: {e}")