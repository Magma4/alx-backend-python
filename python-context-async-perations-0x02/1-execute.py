import mysql.connector
import pymysql
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values
import os
from datetime import datetime

load_dotenv()

class ExecuteQuery:
    def __init__(self, query, params):
        self.connection = None
        self.query = None
        self.params = None

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
    query = "SELECT * FROM user_data WHERE age > '%s'"
    params = (25)

    with ExecuteQuery(query, params) as connection:
        user_data = connection.cursor(cursor=pymysql.cursors.DictCursor)
        user_data.execute(query)
        results = user_data.fetchall()
        
        for row in results:
            print(row)