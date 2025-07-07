from sqlalchemy import Column, String, UUID, Enum as SqlEnum
from uuid import uuid4
from helpers.base import Base
from models.enums.object_type import ObjectType

class BaseObjectORM(Base):
    __abstract__ = True
    id = Column(UUID, primary_key=True, default=uuid4)
    type = Column(SqlEnum(ObjectType), nullable=False)