from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.user_repository import UserRepository
from app.schemas import user_schema


class UserService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = UserRepository(db)

    async def create_user(self, user: user_schema.UserCreate):
        return await self.repo.create_user(user.model_dump())

    async def get_user(self, user_id: str):
        return await self.repo.get_user(user_id)

    async def list_users(self):
        return await self.repo.list_users()

    async def delete_user(self, user_id: str) -> bool:
        return await self.repo.delete_user(user_id)