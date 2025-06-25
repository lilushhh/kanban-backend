import json
from pathlib import Path
from fastapi import HTTPException
from models.task import Task
from helpers.utils import get_next_id
from repositories.projectRepository import get_project_by_id

def get_task_path(project_id: int) -> Path:
    project = get_project_by_id(project_id)
    project_name = project.name.lower().replace(" ", "_")
    return Path("data") / f"tasks_{project_name}.json"

def get_all_tasks(project_id: int):
    path = get_task_path(project_id)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task(**t) for t in data]

def add_task(project_id: int, task: Task):
    project = get_project_by_id(project_id)
    invalid_users = [user for user in task.owners if user not in project.users]
    if invalid_users:
        raise HTTPException(status_code=400, detail=f"Invalid users: {', '.join(invalid_users)}")

    task_list = get_all_tasks(project_id)
    task.id = get_next_id("task")
    task.type = "task"
    task_list.append(task)
    with open(get_task_path(project_id), "w", encoding="utf-8") as f:
        json.dump([t.dict() for t in task_list], f, indent=4)
    return task

def delete_task(project_id: int, task_id: int):
    task_list = get_all_tasks(project_id)
    new_list = [t for t in task_list if t.id != task_id]
    if len(new_list) == len(task_list):
        return False
    with open(get_task_path(project_id), "w", encoding="utf-8") as f:
        json.dump([t.dict() for t in new_list], f, indent=4)
    return True

def update_task_status(project_id: int, task_id: int, new_status: str):
    task_list = get_all_tasks(project_id)
    for t in task_list:
        if t.id == task_id:
            t.status = new_status
            with open(get_task_path(project_id), "w", encoding="utf-8") as f:
                json.dump([task.dict() for task in task_list], f, indent=4)
            return True
    return False


def get_task_by_id(project_id: int, task_id: int):
    task_list = get_all_tasks(project_id)
    return next((t for t in task_list if t.id == task_id), None)
