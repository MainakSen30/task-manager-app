from src.tasks.dtos import TaskSchema as Task
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def create_task(body: Task, db: Session):
    data = body.model_dump()
    # Here you would typically add the task to the database using the db session
    new_task = TaskModel(
        title = data['title'],
        description = data['description'],
        is_completed = data['completed']
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {
        "status": "task created successfully",
        "data": new_task
    }

def get_tasks(db: Session):
    tasks = db.query(TaskModel).all()
    return {
        "status": "All the data retrieved successfully",
        "data": tasks
    }

def get_task_by_id(task_id: int, db: Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail = "Task id incorrect")
    return {
        "status": "task retrieved successfully",
        "data": one_task
    }
