from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.dependencies.auth import hash_password
from app.models.user import USER_COLLECTION


def _to_user(doc: dict | None):
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "username": doc["username"],
        "email": doc["email"],
        "full_name": doc.get("full_name"),
        "role_id": doc.get("role_id"),
        "disabled": int(doc.get("disabled", 0)),
    }


class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_user(self, data: dict):
        plain_password = data.pop("password", None)
        if plain_password:
            data["hashed_password"] = hash_password(plain_password)
        data["disabled"] = int(data.get("disabled", 0))
        result = await self.db[USER_COLLECTION].insert_one(data)
        doc = await self.db[USER_COLLECTION].find_one({"_id": result.inserted_id})
        return _to_user(doc)

    async def get_user(self, user_id: str):
        if not ObjectId.is_valid(user_id):
            return None
        doc = await self.db[USER_COLLECTION].find_one({"_id": ObjectId(user_id)})
        return _to_user(doc)

    async def get_user_by_email(self, email: str):
        doc = await self.db[USER_COLLECTION].find_one({"email": email})
        return doc

    async def get_user_by_username(self, username: str):
        doc = await self.db[USER_COLLECTION].find_one({"username": username})
        return doc

    async def list_users(self):
        docs = await self.db[USER_COLLECTION].find().to_list(length=1000)
        return [_to_user(doc) for doc in docs]

    async def delete_user(self, user_id: str) -> bool:
        if not ObjectId.is_valid(user_id):
            return False
        result = await self.db[USER_COLLECTION].delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0