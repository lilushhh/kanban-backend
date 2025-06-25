from typing import Optional, List
from models.BaseObject import BaseObject
from enum import Enum

class StatusEnum(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "inProgress"
    DONE = "done"

class Task(BaseObject):
    text: str
    owners: Optional[str] = List[str]
    status: StatusEnum