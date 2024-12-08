import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv("MYSQL_USER"),  # Replace with your MySQL username
            password=os.getenv("MYSQL_PASSWORD")  # Replace with your MySQL password
        )
        if connection.is_connected():
            print("Successfully connected to MySQL server")
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")

connection = connect_db()
if connection:
    connection.close()
