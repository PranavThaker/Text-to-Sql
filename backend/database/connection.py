from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    print("DATABASE_URL:", database_url)

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    return database_url


def get_engine():
    database_url = get_database_url()
    return create_engine(database_url)


def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()