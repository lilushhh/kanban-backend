from pydantic import BaseModel
from abc import ABC
from pydantic import Field
from models.enums.object_type import ObjectType
from uuid import UUID, uuid4

class BaseObject(BaseModel, ABC):
    id: UUID = Field(default_factory=uuid4)
    type: ObjectType