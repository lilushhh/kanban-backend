from uuid import UUID
from fastapi import APIRouter, HTTPException
from models.domain.types.project import Project
from repositories.types_repositories.project_repository import (
    get_all, add_item, delete_item, update_item, get_by_id
)
from models.requestes.project_requests import CreateProjectRequest, DeleteProjectRequest, GetProjectByIdRequest, UpdateProjectRequest


router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/")
def read_projects():
    return get_all()

@router.get("/{project_id}")
def read_project_by_id(project_id: UUID):
    returned_project = get_by_id(project_id)
    if returned_project:
        return returned_project
    raise HTTPException(status_code=404, detail="cannot find project")

@router.post("/")
def create_project(project: CreateProjectRequest):
    new_project = Project(
        name = project.name_project,
        users = project.users_list
    )
    project_created = add_item(new_project)
    if project_created:
        return project_created
    raise HTTPException(status_code=404, detail="cannot create project")

@router.delete("/{project_id}")
def delete_project_route(project: DeleteProjectRequest):
    project_to_delete = delete_item(project.project_id)
    if not project_to_delete: 
        raise HTTPException(status_code=404, detail="cannot find project to delete")

@router.put("/{project_id}")
def update_item_route(update: UpdateProjectRequest):
    project_to_update = Project(
        name = update.name_project,
        users = update.users_list,
        id = update.project_id
    )
    updated_project = update_item(project_to_update)
    if updated_project:
        return updated_project
    raise HTTPException(status_code=404, detail="project not found")

