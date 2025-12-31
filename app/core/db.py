import os
import psycopg2

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": 5432,
    "dbname": os.getenv("DB_NAME", "hashd"),
    "user": os.getenv("DB_USER", "hashd"),
    "password": os.getenv("DB_PASSWORD", "hashd"),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)