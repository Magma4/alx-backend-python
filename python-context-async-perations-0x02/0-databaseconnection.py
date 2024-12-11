import mysql.connector
import pymysql
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values
import os
from datetime import datetime

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user=os.getenv("MYSQL_USER"), 
            password=os.getenv("MYSQL_PASSWORD"),
            database='ALX_prodev'
        )
        print("Connection to ALX_prodev database has been opened!")
        return self.connection
    def __exit__(self, type, value, traceback):
        self.connection.close()
        print("Connection to ALX_prodev databse has been closed!")



if __name__ == "__main__":
    query = "SELECT * FROM users"

    with DatabaseConnection() as connection:
        user_data = connection.cursor(cursor=pymysql.cursors.DictCursor)
        user_data.execute(query)
        results = user_data.fetchall()

        print(results)
        for row in results:
            print(row)