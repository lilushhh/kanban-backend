import json
from pathlib import Path
from uuid import UUID
from repositories.types_repositories.project_repository import get_by_id

def get_task_path(project_id: UUID) -> Path:
    project = get_by_id(project_id)
    project_name = project.name.lower().replace(" ", "_")
    return Path("data") / f"tasks_{project_name}.json"
