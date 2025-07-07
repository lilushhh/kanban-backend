from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.orm.orm_types.task_orm import TaskORM
from models.orm.orm_types.project_orm import ProjectORM
from models.domain.types.task import Task
from repositories.base_repository import BaseRepositoryInterface
from helpers.utils import task_to_orm, task_to_pydantic
from uuid import UUID
from typing import List, Optional

class TaskRepositoryDB(BaseRepositoryInterface[Task]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Task]:
        result = await self.db.execute(select(TaskORM))
        return [task_to_pydantic(t) for t in result.scalars().all()]
    
    async def get_by_id(self, item_id: UUID) -> Optional[Task]:
        task = await self.db.get(TaskORM, item_id)
        return task_to_pydantic(task) if task else None
    
    async def add_item(self, item: Task) -> Optional[Task]:
        project = await self.db.get(ProjectORM, item.project_id)
        if not project:
            return None
        invalid_users = [u for u in item.owners if u not in project.users]
        if invalid_users:
            return None
        task_orm = task_to_orm(item)
        self.db.add(task_orm)
        await self.db.commit()
        return item
    
    async def delete_item(self, item_id: UUID) -> bool:
        task = await self.db.get(TaskORM, item_id)
        if not task:
            return False
        await self.db.delete(task)
        await self.db.commit()
        return True
    
    async def update_item(self, item: Task) -> Optional[Task]:
        task = await self.db.get(TaskORM, item.id)
        if not task:
            return None
        task.type = item.type
        task.text = item.text
        task.status = item.status
        task.owners = item.owners
        task.project_id = item.project_id
        await self.db.commit()
        return item
