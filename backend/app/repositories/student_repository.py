from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.student import STUDENT_COLLECTION


def _to_student(doc: dict | None):
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
    }


class StudentRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_student(self, data: dict):
        result = await self.db[STUDENT_COLLECTION].insert_one(data)
        doc = await self.db[STUDENT_COLLECTION].find_one({"_id": result.inserted_id})
        return _to_student(doc)

    async def get_student(self, student_id: str):
        if not ObjectId.is_valid(student_id):
            return None
        doc = await self.db[STUDENT_COLLECTION].find_one({"_id": ObjectId(student_id)})
        return _to_student(doc)

    async def list_students(self):
        docs = await self.db[STUDENT_COLLECTION].find().to_list(length=1000)
        return [_to_student(doc) for doc in docs]

    async def update_student(self, student_id: str, update_data: dict):
        if not ObjectId.is_valid(student_id):
            return None
        await self.db[STUDENT_COLLECTION].update_one(
            {"_id": ObjectId(student_id)},
            {"$set": update_data},
        )
        doc = await self.db[STUDENT_COLLECTION].find_one({"_id": ObjectId(student_id)})
        return _to_student(doc)

    async def delete_student(self, student_id: str) -> bool:
        if not ObjectId.is_valid(student_id):
            return False
        result = await self.db[STUDENT_COLLECTION].delete_one({"_id": ObjectId(student_id)})
        return result.deleted_count > 0