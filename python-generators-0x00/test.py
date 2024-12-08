from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

print(os.getenv("MYSQL_PASSWORD"))