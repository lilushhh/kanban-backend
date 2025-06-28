from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from models.domain.types.project import Project
from models.domain.types.task import Task
from repositories.types_repositories.project_repository import (
    get_all_projects, get_project_by_id, add_project, delete_project, rename_project
)
from repositories.types_repositories.task_repository import (
    get_all_tasks, get_task_by_id,
    add_task, delete_task,
    update_task_status
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- PROJECT ROUTES ----------

@app.get("/projects")
def read_projects():
    return get_all_projects()

@app.get("/projects/{project_id}")
def read_project_by_id(project_id: int):
    return get_project_by_id(project_id)

@app.post("/projects")
def create_project(project: Project):
    add_project(project)
    return {"message": f"Project {project.name} added successfully."}

@app.delete("/projects/{project_id}")
def delete_project_route(project_id: int):
    delete_project(project_id)
    return {"message": "Project deleted successfully"}

@app.put("/projects/{project_id}")
def rename_project_route(project_id: int, newName: str = Query(...)):
    rename_project(project_id, newName)
    return {"message": f"Project renamed to {newName}"}


# ---------- TASK ROUTES ----------

@app.get("/projects/{project_id}/tasks")
def read_tasks(project_id: int):
    return get_all_tasks(project_id)

@app.get("/projects/{project_id}/tasks/{task_id}")
def read_task_by_id(project_id: int, task_id: int):
    return get_task_by_id(project_id, task_id)

@app.post("/projects/{project_id}/tasks")
def add_task_route(project_id: int, task: Task):
    return add_task(project_id, task)

@app.delete("/projects/{project_id}/tasks/{task_id}")
def delete_task_route(project_id: int, task_id: int):
    return delete_task(project_id, task_id)

@app.put("/projects/{project_id}/tasks/{task_id}")
def update_task_status_route(project_id: int, task_id: int, task: Task):
    return update_task_status(project_id, task_id, task.status)
