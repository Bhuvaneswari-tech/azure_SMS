from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.role_repository import RoleRepository
from app.schemas import role_schema


class RoleService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = RoleRepository(db)

    async def create_role(self, role: role_schema.RoleCreate):
        return await self.repo.create_role(role.model_dump())

    async def get_role(self, role_id: str):
        return await self.repo.get_role(role_id)

    async def get_role_by_name(self, name: str):
        return await self.repo.get_role_by_name(name)

    async def list_roles(self):
        return await self.repo.list_roles()

    async def delete_role(self, role_id: str) -> bool:
        return await self.repo.delete_role(role_id)