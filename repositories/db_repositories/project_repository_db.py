from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.orm.orm_types.project_orm import ProjectORM
from models.domain.types.project import Project
from repositories.base_repository import BaseRepositoryInterface
from helpers.utils import project_to_orm, project_to_pydantic
from uuid import UUID, uuid4
from typing import List, Optional

class ProjectRepositoryDB(BaseRepositoryInterface[Project]):
    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_all(self) -> List[Project]:
        result = await self.db.execute(select(ProjectORM))
        return [project_to_pydantic(p) for p in result.scalars().all()]
    
    async def get_by_id(self, item_id: UUID) -> Optional[Project]:
        project = await self.db.get(ProjectORM, item_id)
        return project_to_pydantic(project) if project else None
    
    async def add_item(self, item: Project) -> Optional[Project]:
        existing = await self.db.execute(select(ProjectORM).where(ProjectORM.name == item.name))
        if existing.scalars().first():
            return None
        project_orm = project_to_orm(item)
        self.db.add(project_orm)
        await self.db.commit()
        return item
    
    async def delete_item(self, item_id: UUID) -> bool:
        project = await self.db.get(ProjectORM, item_id)
        if not project:
            return False
        await self.db.delete(project)
        await self.db.commit()
        return True
    
    async def update_item(self, item_id: UUID, item: Project) -> Optional[Project]:
        db_project = await self.db.get(ProjectORM, item_id)
        if not db_project:
            return None
        db_project.id= item_id
        db_project.type = item.type
        db_project.name = item.name
        db_project.users = item.users
        await self.db.commit()
        return item