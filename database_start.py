import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
def setup_table():
    """connect to the database and create the 'conversation' table if
    it doesn't already exist. 
    """
    conn = None
    try:
        # connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        # create the table
        create_table_query ="""
            CREATE TABLE IF NOT EXISTS CONVERSATION (
                id SERIAL PRIMARY KEY,
                user_id varchar(255) NOT NULL,
                user_manager TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT NOW()
            );
            """
        # execute the sql command
        cur.execute(create_table_query)
        conn.commit()
        print("Table 'conversation' have been create successfully or aldready exists")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'error while setting up the database : {error}')
    finally:
        # close the connection
        if conn is not None:
            conn.close()
if __name__ == '__main__':
    setup_table()