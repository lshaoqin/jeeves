import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def connect():
    conn = psycopg2.connect(database=os.getenv("POSTGRES_NAME"), 
                            user=os.getenv("POSTGRES_USER"),
                            password=os.getenv("POSTGRES_PASSWORD"), 
                            host=os.getenv("POSTGRES_HOST"),
                            port=os.getenv("POSTGRES_PORT"))
    
    print("Opened database successfully")
    return conn

def run_operation(sql):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        print("Operation done successfully")
        conn.commit()

        # Record changes to db schema
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
            AND table_type='BASE TABLE';
                    """)
        rows = cur.fetchall()
        with open("schema.txt", "w") as file:
            for row in rows:
                file.write(row[0] + "\n")

        conn.close()

    except Exception as e:
        print("An error occurred: ", e)

def run_query(sql):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    
    except Exception as e:
        print("An error occurred: ", e)
        return None