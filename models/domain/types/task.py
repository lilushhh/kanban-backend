from typing import Optional, List
from uuid import UUID, uuid4
from models.domain.base_object import BaseObject
from models.enums.status_enum import StatusEnum
from models.enums.object_type import ObjectType

class Task(BaseObject):
    text: str
    owners: Optional[str] = List[str]
    status: StatusEnum
    project_id: UUID
    
    def __init__(self, **data):
        data["id"] = uuid4()
        data["type"] = ObjectType.TASK