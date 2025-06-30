from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import List

class CreateProjectRequest(BaseModel):
    name_project: str
    users_list: List[str]

class DeleteProjectRequest(BaseModel):
    project_id: UUID

class GetProjectByIdRequest(BaseModel):
    project_id: UUID

class UpdateProjectRequest(BaseModel):
    project_id: UUID
    name_project: str
    users_list: List[str]
