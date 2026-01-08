import psycopg
import logging
import inspect
import os
from app.settings import (
    DB_NAME,
    DB_USER, DB_PASSWORD,
    DB_HOST, DB_PORT
)

def _who_called_me():
    caller_frame = inspect.stack()[2]
    caller_filename = caller_frame.filename
    return os.path.basename(caller_filename)

def get_database_connection():
    try:
        connection = psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        logging.info(f"Database connection established (call from {_who_called_me()}).")
        return connection
    except Exception:
        logging.exception(f"Database connection failed (call from {_who_called_me()})!")
        return False
    
def close_database_connection(connection):
    try:
        if connection:
            connection.close()
            logging.info(f"Database connection closed (call from {_who_called_me()}).")
    except Exception:
        logging.exception(f"Failed to close database connection (call from {_who_called_me()})!")
        return False