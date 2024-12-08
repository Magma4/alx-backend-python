import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv("MYSQL_USER"), 
            password=os.getenv("MYSQL_PASSWORD"),
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
    except Error as e:
        print(f"There was an error connecting to MySQL: {e}")
        return None


def stream_users():
    connection = connect_db()
    user_data = connection.cursor(dictionary=True) 
    user_data.execute("SELECT * FROM user_data") 

    for row in user_data:  
            yield row

print(next(stream_users()))
