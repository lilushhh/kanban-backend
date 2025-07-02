from typing import List
from uuid import UUID, uuid4
from models.domain.base_object import BaseObject
from models.enums.object_type import ObjectType

class Project(BaseObject):
    name: str
    users: List[str]

    def __init__(self, **data):
        data["id"] = data.get("id", uuid4())
        data["type"] = ObjectType.PROJECT
        super().__init__(**data)