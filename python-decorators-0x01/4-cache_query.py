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
    
def cache_query(func):
    cache = {}  

    def wrapper(connection, query, *args, **kwargs):
        if query in cache: 
            print(f"Query already in cache: {query}")
            return cache[query]
        print(f"Query not in cache: {query}. Executing...")
        result = func(connection, query, *args, **kwargs)
        cache[query] = result 
        return result
    return wrapper

@cache_query
def execute_query(connection, query):
    try:
        user_data = connection.cursor(cursor=pymysql.cursors.DictCursor)
        user_data.execute(query)
        return user_data.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
        return []


if __name__ == "__main__":
    connection = connect_db()
    if connection:
        try:
            query = "SELECT * FROM user_data WHERE age = 25"
            results = execute_query(connection, query)
            print("Results:", results)

            cached_results = execute_query(connection, query)
            print("Cached Results:", cached_results)

        finally:
            connection.close()