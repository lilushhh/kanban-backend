from sqlalchemy import Column, String, UUID
from uuid import uuid4
from database import Base
from enum import Enum
from models.enums.object_type import ObjectType

class BaseObjectORM(Base):
    __abstract__ = True
    id = Column(UUID, primary_key=True, default=uuid4)
    type = Column(Enum(ObjectType), nullable=False)