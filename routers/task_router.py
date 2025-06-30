from uuid import UUID
from fastapi import APIRouter, HTTPException
from models.domain.types.task import Task
from repositories.types_repositories.task_repository import (
    get_all, get_by_id, add_item, delete_item, update_item
)
from models.requestes.task_requests import TasksGetRequest, DeleteTaskRequest,CreateTaskRequest,UpdateTaskRequest,GetTaskByIdRequest

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])

@router.get("/")
def read_tasks():
    return get_all()

@router.get("/{task_id}")
def read_task_by_id(task: GetTaskByIdRequest):
    return get_by_id(task.project_id, task.task_id)

@router.post("/")
def add_task(task: CreateTaskRequest):
    task_new = Task(
        text = task.task_title,
        owners = task.owners_list,
        status = task.status_task,
        project_id = task.project_id
    )
    new_task = add_item(task_new)
    if new_task:
        return new_task
    raise HTTPException(status_code=404, detail="cannot create task")

@router.delete("/{task_id}")
def delete_task_route(task: DeleteTaskRequest):
    task_to_delete = delete_item(task.task_id)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="cannot find task to delete")


@router.put("/{task_id}")
def update_task(update: UpdateTaskRequest):
    task_to_update = Task(
        text = update.task_title,
        owners = update.owners_list,
        status = update.status_task,
        project_id = update.project_id,
        id = update.task_id
    )
    updated_task = update_item(task_to_update)
    if updated_task:
        return updated_task
    raise HTTPException(status_code=404, detail="task not found")
