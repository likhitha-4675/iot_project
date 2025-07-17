from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DB_URL")
print("DB_URL from .env:", db_url)
