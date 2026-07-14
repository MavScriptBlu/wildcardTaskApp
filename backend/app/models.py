"""This is our database table, written as a Python class.
SQLAlchemy turns this into the actual "tasks" table in Postgres.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    due_date = Column(DateTime(timezone=True), nullable=True)

    # created_at/updated_at are set by Postgres itself (server_default/onupdate),
    # not by Python, so they stay correct even if a row is changed outside the app.
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )