from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Create a connection to the database
def db_connect():
    engine = create_engine('postgresql://'+os.getenv("POSTGRES_USER")+':'+os.getenv("POSTGRES_PASSWORD")+'@'+os.getenv("POSTGRES_HOST")+':'+os.getenv("POSTGRES_PORT")+'/'+os.getenv("POSTGRES_NAME"))
    return engine