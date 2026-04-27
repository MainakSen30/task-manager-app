from fastapi import FastAPI
from src.utils.db import Base, engine
from src.tasks.models import TaskModel

Base.metadata.create_all(engine)
app = FastAPI(title="Task Management API",
              description="API for managing tasks with CRUD operations"
              )
print(engine.url)
