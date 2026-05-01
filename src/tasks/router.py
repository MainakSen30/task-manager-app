from fastapi import APIRouter, Depends
from src.utils.db import get_db
from src.tasks import controller
from src.tasks.dtos import TaskSchema as Task
task_routes =  APIRouter(prefix="/tasks")

@task_routes.post("/create")
def create_task(body: Task, db = Depends(get_db)):
    return controller.create_task(body, db)
