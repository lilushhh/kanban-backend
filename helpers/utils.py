import json
from pathlib import Path
from uuid import UUID
from repositories.types_repositories.project_repository import get_by_id

def get_task_path(project_id: UUID) -> Path:
    project = get_by_id(project_id)
    project_name = project.name.lower().replace(" ", "_")
    return Path("data") / f"tasks_{project_name}.json"

def get_next_id(entity: str):
    with open("data/counters.json", "r", encoding="utf-8") as f:
        counters = json.load(f)
    key = f"last_{entity}_id"
    new_id = counters.get(key, 0) + 1
    counters[key] = new_id
    with open("data/counters.json", "r", encoding="utf-8") as f:
        json.dump(counters, f, indent=4)
    return new_id