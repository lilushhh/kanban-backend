import json
from uuid import UUID, uuid4
from pathlib import Path
from fastapi import HTTPException
from typing import List, Optional
from models.domain.types.task import Task
from models.requestes.task_requests import TasksGetRequest, CreateTaskRequest, DeleteTaskRequest, UpdateTaskRequest, GetTaskByIdRequest
from models.requestes.project_requests import GetProjectByIdRequest
from helpers.utils import get_task_path
from repositories.types_repositories.project_repository import get_by_id
from repositories.base_repository import BaseRepositoryInterface

task_json_path = Path("data/tasksProjects.json")

class TaskRepository(BaseRepositoryInterface[Task]):
    def get_all(self) -> List[Task]:
        if not task_json_path.exists():
            return []
        with open(task_json_path, "r", encoding="utf-8") as tasks_json:
            data = json.load(tasks_json)
        return [Task(**item) for item in data]

    
    def add_item(self, item: Task) -> Task:
        project = get_by_id(Task.project_id)
        invalid_users = [user for user in item.owners_list if user not in project.users]
        if invalid_users:
            raise HTTPException(status_code=400, detail=f"Invalid users: {', '.join(invalid_users)}")

        tasks = self.get_all()
        tasks.append(item)
        with open(task_json_path, "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in tasks], f, indent=4)
        return item


    
    def delete_item(self, task_id_to_delete: UUID) -> bool:
        tasks = self.get_all()
        after_delete_tasks = [t for t in tasks if t.id != task_id_to_delete]
        if len(tasks) != len(after_delete_tasks): return False
        with open(task_json_path, "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in after_delete_tasks], f, indent=4)
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

    
    def get_by_id(self, task_to_get: GetTaskByIdRequest) -> Optional[Task]:
        task_list = self.get_all(task_to_get.project_id)
        return next((t for t in task_list if t.id == task_to_get.task_id), None)