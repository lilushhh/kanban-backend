import json
from pathlib import Path
from models.project import Project
from helpers.utils import get_next_id

project_json_path= Path("data/projects.json")

def get_all_projects():
    with open(project_json_path, 'r', encoding='utf-8') as project_json:
        data = json.load(project_json)
    return [Project(**item) for item in data]

def get_project_by_id(project_id: int):
    projects = get_all_projects()
    return next((p for p in projects if p.id == project_id), None)

def add_project(project):
    projects_list = get_all_projects()

    if not any(p.name == project.name for p in projects_list):
        project.id = get_next_id("project")
        project.type = "project"

        projects_list.append(project)
        with open(project_json_path, 'w', encoding='utf-8') as file:
            json.dump([p.dict() for p in projects_list], file, indent=4)

        task_filename = f'tasks_{project.name.lower().replace(" ", "_")}.json'
        task_folder = Path("data")
        task_path = task_folder / task_filename

        with open(task_path, 'w', encoding='utf-8') as task_file:
            json.dump([], task_file, indent=4)

def delete_project(project_id: int):
    projects = get_all_projects()
    projects_after_delete = [project for project in projects if project.id != project_id]
    if len(projects) == len(projects_after_delete):
        return False
    else:
        with open(project_json_path, "w", encoding="utf-8") as f:
            json.dump([p.dict() for p in projects_after_delete], f, indent=4)
        return True
    
def rename_project(project_id: int, new_name: str):
    projects = get_all_projects()
    for p in projects:
        if p.id == project_id:
            p.name = new_name
            with open(project_json_path, "w", encoding="utf-8") as f:
                json.dump([pr.dict() for pr in projects], f, indent=4)
            return True
    return False

