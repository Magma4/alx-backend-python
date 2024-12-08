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
    
def stream_users_in_batches(batch_size):
    connection = connect_db()
    if not connection:
        print("Could not connect to the database.")
        return

    try:
        user_data = connection.cursor(cursor=pymysql.cursors.DictCursor)
        user_data.execute("SELECT * FROM user_data")

        while True:
            batch = user_data.fetchmany(batch_size)
            if batch == None:
                break
            yield batch

    except pymysql.MySQLError as e:
        print(f"There was an error fetching data: {e}")
    finally:
        connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_users_under_25 = [user for user in batch if user['age'] > 25] 
        yield filtered_users_under_25

if __name__ == "__main__":
    batch_size = 5  
    for batch in batch_processing(batch_size):
        for user in batch:
            print(user)