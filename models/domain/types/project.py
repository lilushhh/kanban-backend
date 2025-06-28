from typing import List
from models.domain.base_object import BaseObject

class Project(BaseObject):
    name: str
    users: List[str]