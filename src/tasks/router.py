from fastapi import APIRouter, Depends
from src.utils.db import get_db
from src.tasks import controller
from src.tasks.dtos import TaskSchema as Task

task_routes =  APIRouter(prefix="/tasks")

@task_routes.post("/create")
def create_task(body: Task, db = Depends(get_db)):
    return controller.create_task(body, db)

@task_routes.get("/all_tasks")
def get_all_tasks(db = Depends(get_db)):
    return controller.get_tasks(db)

@task_routes.get("/one_task/{task_id}")
def get_task_by_id(task_id: int, db = Depends(get_db)):
    return controller.get_task_by_id(task_id, db)

@task_routes.put("/update_task/{task_id}")
def update_task(task_id: int, body: Task, db = Depends(get_db)):
    return controller.update_task(task_id, body, db)

@task_routes.delete("/delete_task/{task_id}")
def delete_task(task_id: int, db = Depends(get_db)):
    return controller.delete_task(task_id, db)
