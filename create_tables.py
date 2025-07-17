from sqlalchemy import create_engine
from models.models import metadata
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)
metadata.create_all(engine)

print("Tables created in your database.")
