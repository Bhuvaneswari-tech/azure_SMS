from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.role import ROLE_COLLECTION


def _to_role(doc: dict | None):
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
    }


class RoleRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_role(self, data: dict):
        result = await self.db[ROLE_COLLECTION].insert_one(data)
        doc = await self.db[ROLE_COLLECTION].find_one({"_id": result.inserted_id})
        return _to_role(doc)

    async def get_role(self, role_id: str):
        if not ObjectId.is_valid(role_id):
            return None
        doc = await self.db[ROLE_COLLECTION].find_one({"_id": ObjectId(role_id)})
        return _to_role(doc)

    async def get_role_by_name(self, name: str):
        doc = await self.db[ROLE_COLLECTION].find_one({"name": name})
        return _to_role(doc)

    async def list_roles(self):
        docs = await self.db[ROLE_COLLECTION].find().to_list(length=1000)
        return [_to_role(doc) for doc in docs]

    async def delete_role(self, role_id: str) -> bool:
        if not ObjectId.is_valid(role_id):
            return False
        result = await self.db[ROLE_COLLECTION].delete_one({"_id": ObjectId(role_id)})
        return result.deleted_count > 0