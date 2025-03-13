from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from lux.utils.settings import settings

DEFAULT_DATABASE_URL = "sqlite:///:memory:"

database_url = settings.get('database.url', DEFAULT_DATABASE_URL)

engine = create_engine(
    database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
