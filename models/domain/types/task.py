from typing import Optional, List
from models.domain.base_object import BaseObject
from models.enums.status_enum import StatusEnum

class Task(BaseObject):
    text: str
    owners: Optional[str] = List[str]
    status: StatusEnum