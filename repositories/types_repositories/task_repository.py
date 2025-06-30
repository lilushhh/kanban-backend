import json
from uuid import UUID, uuid4
from fastapi import HTTPException
from typing import List, Optional
from models.domain.types.task import Task
from models.requestes.task_requests import TasksGetRequest, CreateTaskRequest, DeleteTaskRequest, UpdateTaskRequest, GetTaskByIdRequest
from models.requestes.project_requests import GetProjectByIdRequest
from helpers.utils import get_task_path
from repositories.types_repositories.project_repository import get_by_id
from repositories.base_repository import BaseRepositoryInterface

class TaskRepository(BaseRepositoryInterface[Task]):
    def get_all(self, tasks_get: TasksGetRequest) -> List[Task]:
        path = get_task_path(tasks_get.project_id)
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Task(**t) for t in data]
    
    def add_item(self, item: CreateTaskRequest) -> Task:
        project = get_by_id(GetProjectByIdRequest(project_id = item.project_id))
        invalid_users = [user for user in item.owners_list if user not in project.users]
        if invalid_users:
            raise HTTPException(status_code=400, detail=f"Invalid users: {', '.join(invalid_users)}")

        task_list = self.get_all(item.project_id)

        task_list.append(item)
        with open(self.get_task_path(item.project_id), "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in task_list], f, indent=4)
        return item
    
    def delete_item(self, task_to_delete: DeleteTaskRequest) -> bool:
        task_list = self.get_all(task_to_delete.project_id)
        new_list = [t for t in task_list if t.id != task_to_delete.task_id]
        if len(new_list) == len(task_list):
            return False
        with open(self.get_task_path(task_to_delete.project_id), "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in new_list], f, indent=4)
        return True
    
    def update_item(self, updated_task: UpdateTaskRequest) -> Task:
        task_list = self.get_all(updated_task.project_id)
        for i, task in enumerate(task_list):
            if task.id == updated_task.task_id:
                updated_task_obj = task.copy(update={
                    "text": updated_task.task_title,
                    "owners": updated_task.owners_list,
                    "status": updated_task.status_task
                })
                task_list[i] = updated_task_obj
                with open(self.get_task_path(updated_task.project_id), "w", encoding="utf-8") as f:
                    json.dump([t.dict() for t in task_list], f, indent=4)
                return updated_task_obj
        raise HTTPException(status_code=404, detail="Task not found")

    
    def get_by_id(self, project_id: UUID, task_id: UUID) -> Optional[Task]:
        task_list = self.get_all(project_id)
        return next((t for t in task_list if t.id == task_id), None)