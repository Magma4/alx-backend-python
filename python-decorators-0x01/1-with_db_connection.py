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

@with_db_connection
def fetch_users(connection):
    try:
        user_data = connection.cursor(cursor=pymysql.cursors.DictCursor)
        user_data.execute("SELECT * FROM user_data WHERE name = 'Kristin Daniel'")
        return user_data.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error fetching users: {e}")
        return []
    
if __name__ == "__main__":
    users = fetch_users()
    print("Users:", users)