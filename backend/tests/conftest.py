import os
import pytest

from sqlalchemy import create_engine,text
from sqlalchemy.arm import sessionmaker

@pytest.fixture(scope='session')
def test_database_url():
    
    url = os.getenv('TEST_DATABASE_URL')
    if not url:
        raise RuntimeError(
            "TEST_DATABASE_URL is not set"
        )
        
    return url

@pytest.fixture(scope='session')
def test_engine(test_database_url):
    engine = create_engine(test_database_url)

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        engine.dispose()
        raise

    yield engine

    engine.dispose()
    

@pytest.fixture(scope="session")
def test_session_factory(test_engine):

    return sessionmaker(
        bind=test_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


@pytest.fixture
def db_session(test_session_factory):

    session = test_session_factory()

    try:
        yield session
        session.rollback()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()