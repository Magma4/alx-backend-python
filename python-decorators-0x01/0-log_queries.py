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
    
def log_queries(func):
    
    def wrapper(*args, **kwargs):
        query = args[1] 
        print(f"{datetime.now()}: called {func.__name__} with args {args}")
        print(f"{datetime.now()}: called {func.__name__} returned {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def execute_query(connection, query):
    """
    Execute a SQL query on the database.
    """
    try:
        user_data = connection.cursor()
        user_data.execute(query)
        if query:
            print("Query executed successfully.")
            return user_data.fetchall()  
        else:
            connection.commit()  
            print("No queries found")
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")


if __name__ == "__main__":
    connection = connect_db()
    if connection:
        query = "SELECT * FROM user_data WHERE age = 25"
        results = execute_query(connection, query)
        print(results)
        connection.close()