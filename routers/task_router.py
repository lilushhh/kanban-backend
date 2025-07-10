from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db_config import get_db
from models.domain.types.task import Task
from repositories.db_repositories.task_repository_db import TaskRepositoryDB
from models.requestes.task_requests import (
    CreateTaskRequest,
    UpdateTaskRequest
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepositoryDB:
    return TaskRepositoryDB(db)

@router.get("/")
async def read_tasks(task_repo: TaskRepositoryDB = Depends(get_task_repo)):
    return await task_repo.get_all()

@router.get("/{task_id}")
async def read_task_by_id(task_id: UUID, task_repo: TaskRepositoryDB = Depends(get_task_repo)):
    task = await task_repo.get_by_id(task_id)
    if task:
        return task
    raise HTTPException(status_code=404, detail="task not found")

@router.post("/")
async def add_task(task: CreateTaskRequest, task_repo: TaskRepositoryDB = Depends(get_task_repo)):
    task_new = Task(
        text=task.task_title,
        owners=task.owners_list,
        status=task.status_task,
        project_id=task.project_id
    )
    new_task = await task_repo.add_item(task_new)
    if new_task:
        return new_task
    raise HTTPException(status_code=400, detail="cannot create task")

@router.put("/{task_id}")
async def update_task(task_id: UUID, update: UpdateTaskRequest, task_repo: TaskRepositoryDB = Depends(get_task_repo)):
    task_to_update = Task(
        id=task_id,
        text=update.text,
        owners=update.owners_list,
        status=update.status_task,
        project_id=update.project_id
    )
    updated_task = await task_repo.update_item(task_to_update)
    if updated_task is None:
        existing_task = await task_repo.get_by_id(task_id)
        if existing_task is None:
            raise HTTPException(status_code=404, detail="task not found")
        else:
            raise HTTPException(status_code=400, detail="cannot update task")
    return updated_task

@router.delete("/{task_id}")
async def delete_task(task_id: UUID, task_repo: TaskRepositoryDB = Depends(get_task_repo)):
    task_to_delete = await task_repo.delete_item(task_id)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="cannot find task to delete")
    return {"message": "Task deleted successfully"}
