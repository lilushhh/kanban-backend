from sqlalchemy import Column, String, JSON, UUID, ForeignKey, Enum as SqlEnum
from models.orm.base_object_orm import BaseObjectORM
from models.enums.status_enum import StatusEnum

class TaskORM(BaseObjectORM):
    __tablename__ = "tasks"
    text = Column(String, nullable=False)
    owners = Column(JSON, default=[], nullable=False)
    status = Column(SqlEnum(StatusEnum), nullable=False)
    project_id = Column(UUID, ForeignKey("projects.id"), nullable=False)
