from uuid import UUID
from pydantic import BaseModel
from typing import List
from models.enums.status_enum import StatusEnum

class TasksGetRequest(BaseModel):
    project_id: UUID

class CreateTaskRequest(BaseModel):
    project_id: UUID
    task_title: str
    owners_list: List[str]
    status_task: StatusEnum

class DeleteTaskRequest(BaseModel):
    task_id: UUID

class UpdateTaskRequest(BaseModel):
    project_id: UUID
    task_id: UUID
    task_title: str
    owners_list: List[str]
    status_task: StatusEnum

class GetTaskByIdRequest(BaseModel):
    task_id: UUID
    