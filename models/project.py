from typing import List
from models.BaseObject import BaseObject

class Project(BaseObject):
    name: str
    users: List[str]