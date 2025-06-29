from uuid import UUID
from fastapi import APIRouter, Query
from models.domain.types.project import Project
from repositories.types_repositories.project_repository import (
    get_all, add_item, delete_item, update_item, get_by_id
)

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/")
def read_projects():
    return get_all()

@router.get("/{project_id}")
def read_project_by_id(project_id: UUID):
    return get_by_id(project_id)

@router.post("/")
def create_project(project: Project):
    return add_item(project)

@router.delete("/{project_id}")
def delete_project_route(project_id: UUID):
    return delete_item(project_id)

@router.put("/{project_id}")
def update_item_route(project_id: UUID, updated_project: Project):
    return update_item(project_id, updated_project)

