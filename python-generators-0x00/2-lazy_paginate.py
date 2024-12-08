import mysql.connector
import pymysql
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

def connect_db():
    """Connect to the MySQL server."""
    try:
        connection = pymysql.connect(
            host='localhost',
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database='ALX_prodev'
        )
        print("Successfully connected to MySQL server")
        return connection
    except pymysql.MySQLError as e:
        print(f"There was an error connecting to MySQL: {e}")
        return None

def paginate_users(page_size, offset):
    try:
        user_data = connect_db().cursor(cursor=pymysql.cursors.DictCursor)
        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        user_data.execute(query)
        return user_data.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error fetching paginated data: {e}")
        return []

def lazy_paginate(page_size):
    connection = connect_db()
    if not connection:
        print("Error connecting to the database.")
        return

    try:
        offset = 0
        while True:
            page = paginate_users( page_size, offset)
            if not page:  
                break
            yield page
            offset += page_size
    finally:
        connection.close()


if __name__ == "__main__":
    page_size = 5
    for page in lazy_paginate(page_size):
        for user in page:
            print(user)