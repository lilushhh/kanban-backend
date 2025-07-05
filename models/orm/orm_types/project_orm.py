from sqlalchemy import Column, String, JSON
from models.orm.base_object_orm import BaseObjectORM

class ProjectORM(BaseObjectORM):
    __tablename__ = "projects"
    name = Column(String, nullable=False)
    users = Column(JSON, default=[], nullable=False)