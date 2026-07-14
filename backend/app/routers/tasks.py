"""
All the create/view/update/delete logic for tasks live here.
Each function below is one API endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

# Every route in this file is grouped under /tasks.
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=schemas.TaskRead, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Add a new task to the list."""
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()

    # Reload from the database so the response includes fields Postgres fills
    # in itself, like the generated id and timestamps.
    db.refresh(new_task)
    return new_task


@router.get("", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    """Get every task, newest first."""
    return db.query(models.Task).order_by(models.Task.created_at.desc()).all()


@router.get("/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single task by its ID."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, updates: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Change one or more fields on an existing task."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # exclude_unset=True skips any field the caller didn't send, so a partial
    # update only touches the fields that were actually included.
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Remove a task for good. This is permanent and cannot be undone."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None