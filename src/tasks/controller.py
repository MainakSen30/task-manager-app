from src.tasks.dtos import TaskSchema as Task
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
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
