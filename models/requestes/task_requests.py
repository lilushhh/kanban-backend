from uuid import UUID
from pydantic import BaseModel, Field
from typing import List
from models.enums.status_enum import StatusEnum

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
    text: str = Field(..., alias="task_title")
    owners_list: List[str]
    status_task: StatusEnum
    class Config:
        allow_population_by_field_name = True


class GetTaskByIdRequest(BaseModel):
    task_id: UUID
    