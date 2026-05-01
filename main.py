from fastapi import FastAPI
from src.utils.db import Base, engine
from src.tasks.router import task_routes

Base.metadata.create_all(engine)
app = FastAPI(title="Task Management API",
              description="API for managing tasks with CRUD operations")
app.include_router(task_routes)
