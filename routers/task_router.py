from uuid import UUID
from fastapi import APIRouter, HTTPException
from models.domain.types.task import Task
from repositories.db_repositories.task_repository_db import TaskRepositoryDB
from models.requestes.task_requests import (
    CreateTaskRequest,
    UpdateTaskRequest
)

router = APIRouter(prefix="/tasks", tags=["tasks"])
task_repo = TaskRepositoryDB()

@router.get("/")
def read_tasks():
    return task_repo.get_all()

@router.get("/{task_id}")
def read_task_by_id(task_id: UUID):
    task = task_repo.get_by_id(task_id)
    if task:
        return task
    raise HTTPException(status_code=404, detail="task not found")

@router.post("/")
def add_task(task: CreateTaskRequest):
    task_new = Task(
        text=task.task_title,
        owners=task.owners_list,
        status=task.status_task,
        project_id=task.project_id
    )
    new_task = task_repo.add_item(task_new)
    if new_task:
        return new_task
    raise HTTPException(status_code=400, detail="cannot create task")

@router.put("/{task_id}")
def update_task(task_id: UUID, update: UpdateTaskRequest):
    task_to_update = Task(
        id=task_id,
        text=update.task_title,
        owners=update.owners_list,
        status=update.status_task,
        project_id=update.project_id
    )
    updated_task = task_repo.update_item(task_to_update)
    if updated_task:
        return updated_task
    raise HTTPException(status_code=404, detail="task not found")

@router.delete("/{task_id}")
def delete_task(task_id: UUID):
    task_to_delete = task_repo.delete_item(task_id)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="cannot find task to delete")
    return {"message": "Task deleted successfully"}
