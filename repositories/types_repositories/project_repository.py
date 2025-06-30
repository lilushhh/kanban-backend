import json
from pathlib import Path
from uuid import UUID, uuid4
from typing import List
from fastapi import HTTPException
from models.requestes.project_requests import CreateProjectRequest, DeleteProjectRequest, GetProjectByIdRequest, UpdateProjectRequest
from models.domain.types.project import Project
from repositories.base_repository import BaseRepositoryInterface

project_json_path = Path("data/projects.json")

class ProjectRepository(BaseRepositoryInterface[Project]):
    def get_all(self) -> List[Project]:
        if not project_json_path.exists():
            return []
        with open(project_json_path, 'r', encoding='utf-8') as project_json:
            data = json.load(project_json)
        return [Project(**item) for item in data]
    
    def add_item(self, project: CreateProjectRequest) -> Project:
        projects_list = self.get_all()

        if any(p.name == project.name for p in projects_list):
            raise HTTPException(status_code=400, detail="Project name already exists")

        
        project_to_add = Project(
            name = project.name_project,
            users = project.users_list
        )

        projects_list.append(project_to_add)

        with open(project_json_path, 'w', encoding='utf-8') as file:
            json.dump([p.dict() for p in projects_list], file, indent=4)

        task_filename = f'tasks_{project.name.lower().replace(" ", "_")}.json'
        task_folder = Path("data")
        task_path = task_folder / task_filename

        with open(task_path, 'w', encoding='utf-8') as task_file:
            json.dump([], task_file, indent=4)

        return project
    
    def delete_item(self, project_to_delete: DeleteProjectRequest) -> bool:
        projects = self.get_all()
        projects_after_delete = [p for p in projects if p.id != project_to_delete.project_id]
        if len(projects) == len(projects_after_delete):
            return False
        with open(project_json_path, "w", encoding="utf-8") as f:
            json.dump([p.dict() for p in projects_after_delete], f, indent=4)
        return True
    
    def update_item(self, updated_project: UpdateProjectRequest) -> Project:
        projects = self.get_all()
        for i, p in enumerate(projects):
            if p.id == updated_project.project_id:
                projects[i] = updated_project.copy(update={"id": updated_project.project_id})
                with open(project_json_path, "w", encoding="utf-8") as f:
                    json.dump([pr.dict() for pr in projects], f, indent=4)
                return projects[i]
        raise HTTPException(status_code=404, detail="Project not found")
    
    def get_by_id(self, project_to_get: GetProjectByIdRequest):
        projects = self.get_all()
        return next((project for project in projects if project.id == project_to_get.project_id), None)