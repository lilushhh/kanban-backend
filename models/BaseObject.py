from pydantic import BaseModel
from typing import Optional
from enum import Enum

class objectType(str, Enum):
    PROJECT = "project"
    TASK = "task"

class BaseObject(BaseModel):
    id: Optional[int]
    type: Optional[objectType]