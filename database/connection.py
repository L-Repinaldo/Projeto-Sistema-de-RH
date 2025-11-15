import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

def db_connection():


    try:
        conn = psycopg2.connect(
                                    user = os.getenv('DB_USER') ,
                                    password = os.getenv('DB_PASS') ,
                                    host = os.getenv('DB_HOST') ,
                                    port = os.getenv('DB_PORT')  )

        conn.autocommit = True 
        
        return conn
        
    except psycopg2.DatabaseError as error:

        print("Unable to connect to the Database")

        print("XXXXXXXXXXXXXXXXX")

        print(error)

        return None