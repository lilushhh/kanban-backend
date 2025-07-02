import json
from uuid import UUID, uuid4
from pathlib import Path
from fastapi import HTTPException
from typing import List, Optional
from models.domain.types.task import Task
from repositories.types_repositories.project_repository import ProjectRepository
from repositories.base_repository import BaseRepositoryInterface
from helpers.utils import to_serializable

task_json_path = Path("data/tasksProjects.json")
project_repo = ProjectRepository()

class TaskRepository(BaseRepositoryInterface[Task]):
    def get_all(self) -> List[Task]:
        if not task_json_path.exists():
            return []
        with open(task_json_path, "r", encoding="utf-8") as tasks_json:
            data = json.load(tasks_json)
        return [Task(**item) for item in data]

    
    def add_item(self, item: Task) -> Optional[Task]:
        project = project_repo.get_by_id(item.project_id)
        invalid_users = [user for user in item.owners if user not in project.users]
        if invalid_users:
            return None

        tasks = self.get_all()
        tasks.append(item)
        with open(task_json_path, "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in tasks], f, indent=4, default=to_serializable)
        return item


    def delete_item(self, task_id_to_delete: UUID) -> bool:
        tasks = self.get_all()
        after_delete_tasks = [t for t in tasks if t.id != task_id_to_delete]
        if len(tasks) == len(after_delete_tasks): return False
        with open(task_json_path, "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in after_delete_tasks], f, indent=4, default=to_serializable)
        return True
    

    def update_item(self, updated_task: Task) -> Optional[Task]:
        tasks = self.get_all()
        for i, t in enumerate(tasks):
            if t.id == updated_task.id:
                tasks[i] = updated_task.copy(update={
                "id": t.id,
                "project_id": t.project_id})
                with open(task_json_path, "w", encoding= "utf-8") as f:
                    json.dump([t.dict() for t in tasks], f, indent=4, default=to_serializable)
                return tasks[i]
        return None

    
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        tasks = self.get_all()
        return next((t for t in tasks if t.id == task_id), None)