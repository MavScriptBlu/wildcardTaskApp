"""
This sets up the connection to PostgreSQL using SQLAlchemy.
Every route that needs to touch the database borrows a "session" from this file, which is a connection to the database that can be used to query and update data.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)

# Each request gets its own session, kind of like its own conversation with the
# database. This is a factory that makes sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Every table model in this app inherits from this.
Base = declarative_base()


def get_db():
    """
    FastAPI calls this for any route that needs the database.
    Hands out a session, then makes sure it's closed when the request is done.
    """
    db = SessionLocal()
    try:
        # Yielding (instead of returning) lets FastAPI run the route first and
        # come back here afterward to clean up, even if the route raised an error.
        yield db
    finally:
        db.close()