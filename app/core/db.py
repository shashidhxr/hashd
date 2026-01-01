import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": 5432,
    "dbname": os.getenv("DB_NAME", "hashd"),
    "user": os.getenv("DB_USER", "hashd"),
    "password": os.getenv("DB_PASSWORD", "hashd"),
}

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_CONFIG.user}:{DB_CONFIG.password}"
    f"@{DB_CONFIG.host}:5432/{DB_CONFIG.name}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

sessionLocal = sessionmaker(
    bind=engine,
    autoCommit=False,
    autoflush=False
)

def get_connection():
    return psycopg2.connect(**DB_CONFIG)