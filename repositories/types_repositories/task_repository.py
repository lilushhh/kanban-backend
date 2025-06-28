import json
from uuid import UUID, uuid4
from fastapi import HTTPException
from typing import List, Optional
from models.domain.types.task import Task
from helpers.utils import get_task_path
from repositories.types_repositories.project_repository import get_by_id
from repositories.base_repository import BaseRepositoryInterface

class TaskRepository(BaseRepositoryInterface[Task]):
    def get_all(self, project_id: UUID) -> List[Task]:
        path = get_task_path(project_id)
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task(**t) for t in data]
    
    def add_item(self, item: Task, project_id: UUID) -> Task:
        project = get_by_id(project_id)
        invalid_users = [user for user in item.owners if user not in project.users]
        if invalid_users:
            raise HTTPException(status_code=400, detail=f"Invalid users: {', '.join(invalid_users)}")

        task_list = self.get_all(project_id)
        item.id = uuid4()
        item.type = "task"
        task_list.append(item)
        with open(self.get_task_path(project_id), "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in task_list], f, indent=4)
        return item
    
    def delete_item(self, item_id: UUID, project_id: UUID) -> bool:
        task_list = self.get_all(project_id)
        new_list = [t for t in task_list if t.id != item_id]
        if len(new_list) == len(task_list):
            return False
        with open(self.get_task_path(project_id), "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in new_list], f, indent=4)
        return True
    
    def update_item(self, item_id: UUID, new_item: Task, project_id: UUID) -> Task:
        task_list = self.get_all(project_id)
        for i, t in enumerate(task_list):
            if t.id == item_id:
                task_list[i] = new_item.copy(update={"id": item_id})
                with open(self.get_task_path(project_id), "w", encoding="utf-8") as f:
                    json.dump([task.dict() for task in task_list], f, indent=4)
                return task_list[i]
        raise HTTPException(status_code=404, detail="Task not found")
    
    def get_by_id(self, project_id: UUID, task_id: UUID) -> Optional[Task]:
        task_list = self.get_all(project_id)
        return next((t for t in task_list if t.id == task_id), None)