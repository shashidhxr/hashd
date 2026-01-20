import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = 5432
DB_NAME = os.getenv("DB_NAME", "hashd")
DB_USER = os.getenv("DB_USER", "hashd")
DB_PASSWORD = os.getenv("DB_PASSWORD", "hashd")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:5432/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

sessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# def get_connection():
#     return psycopg2.connect(**DB_CONFIG)