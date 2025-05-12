import pytest
import psycopg2
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def db_connection():
    for _ in range(5):
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5433,
                user="test",
                password="test",
                dbname="testdb"
            )
            yield conn
            conn.close()
            break
        except psycopg2.OperationalError:
            time.sleep(1)
    else:
        pytest.fail("Не удалось подключиться к тестовой БД")


@pytest.fixture
def db_session(db_connection):
    engine = create_engine("postgresql+psycopg2://", creator=lambda: db_connection)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()