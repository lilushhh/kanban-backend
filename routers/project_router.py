from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db_config import get_db
from models.domain.types.project import Project
from repositories.db_repositories.project_repository_db import ProjectRepositoryDB
from models.requestes.project_requests import CreateProjectRequest, UpdateProjectRequest

router = APIRouter(prefix="/projects", tags=["projects"])
project_repo = ProjectRepositoryDB()

def get_project_repo(db: AsyncSession = Depends(get_db)) -> ProjectRepositoryDB:
    return ProjectRepositoryDB(db)

@router.get("/")
def read_projects():
    return project_repo.get_all()

@router.get("/{project_id}")
def read_project_by_id(project_id: UUID):
    returned_project = project_repo.get_by_id(project_id)
    if returned_project:
        return returned_project
    raise HTTPException(status_code=404, detail="cannot find project")

@router.post("/")
def create_project(project: CreateProjectRequest):
    new_project = Project(
        name=project.name_project,
        users=project.users_list
    )
    project_created = project_repo.add_item(new_project)
    if project_created:
        return project_created
    raise HTTPException(status_code=400, detail="cannot create project")

@router.delete("/{project_id}")
def delete_project(project_id: UUID):
    project_to_delete = project_repo.delete_item(project_id)
    if not project_to_delete:
        raise HTTPException(status_code=404, detail="cannot find project to delete")
    return {"message": "Project deleted successfully"}

@router.put("/{project_id}")
def update_project(project_id: UUID, update: UpdateProjectRequest):
    project_to_update = Project(
        id=project_id,
        name=update.name_project,
        users=update.users_list
    )
    updated_project = project_repo.update_item(project_to_update)
    if updated_project:
        return updated_project
    raise HTTPException(status_code=404, detail="project not found")
