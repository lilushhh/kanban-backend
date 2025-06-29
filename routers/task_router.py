from uuid import UUID
from fastapi import APIRouter
from models.domain.types.task import Task
from repositories.types_repositories.task_repository import (
    get_all, get_by_id, add_item, delete_item, update_item
)

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])

@router.get("/")
def read_tasks(project_id: UUID):
    return get_all(project_id)

@router.get("/{task_id}")
def read_task_by_id(project_id: UUID, task_id: UUID):
    return get_by_id(project_id, task_id)

@router.post("/")
def add_task(project_id: UUID, task: Task):
    return add_item(project_id, task)

@router.delete("/{task_id}")
def delete_task_route(project_id: UUID, task_id: UUID):
    return delete_item(project_id, task_id)

@router.put("/{task_id}")
def update_task(project_id: UUID, task_id: UUID, new_task: Task):
    return update_item(task_id, new_task, project_id)