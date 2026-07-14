"""
These describe the "shape" of a task going in and out of the API.
Basically the rules for what counts as a valid task, separate from 
what the database table actually looks like.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    """The base class for a task, which is used for both input and output."""

    # Lets Pydantic build this straight from a SQLAlchemy object's attributes,
    # not just from a dict, so routes can return ORM rows directly.
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """What we expect when someone creates a new task. Same shape as the base."""

    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    Everything's optional here since you might only want to change one field,
    like just checking a task off as completed. You don't have to send the
    whole task back.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class TaskRead(TaskBase):
    """What we send back to the frontend."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)