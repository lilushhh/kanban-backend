from enum import Enum
from uuid import UUID
from models.orm.orm_types.project_orm import ProjectORM
from models.orm.orm_types.task_orm import TaskORM
from models.domain.types.project import Project
from models.domain.types.task import Task


def to_serializable(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, Enum):
        return obj.value
    return str(obj)

def project_to_pydantic(project_orm: ProjectORM) -> Project:
    return Project(
        id = project_orm.id,
        type = project_orm.type,
        name = project_orm.name,
        users = project_orm.users
    )

def project_to_orm(project_pydantic: Project) -> ProjectORM:
    return ProjectORM(
        id = str(project_pydantic.id),
        type = project_pydantic.type,
        name = project_pydantic.name,
        users = project_pydantic.users
    )

def task_to_pydantic(task_orm: TaskORM) -> Task:
    return Task(
        id = task_orm.id,
        text = task_orm.text,
        type = task_orm.type,
        owners = task_orm.owners,
        status = task_orm.status,
        project_id = task_orm.project_id
    )

def task_to_orm(task_pydantic: Task) -> TaskORM:
    return TaskORM(
        id = str(task_pydantic.id),
        text = task_pydantic.text,
        type = task_pydantic.type,
        owners = task_pydantic.owners,
        status = task_pydantic.status,
        project_id = task_pydantic.project_id
    )