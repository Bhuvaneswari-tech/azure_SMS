from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.course import COURSE_COLLECTION


def _to_course(doc: dict | None):
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "title": doc["title"],
        "description": doc.get("description"),
    }


class CourseRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_course(self, data: dict):
        result = await self.db[COURSE_COLLECTION].insert_one(data)
        doc = await self.db[COURSE_COLLECTION].find_one({"_id": result.inserted_id})
        return _to_course(doc)

    async def get_course(self, course_id: str):
        if not ObjectId.is_valid(course_id):
            return None
        doc = await self.db[COURSE_COLLECTION].find_one({"_id": ObjectId(course_id)})
        return _to_course(doc)

    async def list_courses(self):
        docs = await self.db[COURSE_COLLECTION].find().to_list(length=1000)
        return [_to_course(doc) for doc in docs]

    async def update_course(self, course_id: str, update_data: dict):
        if not ObjectId.is_valid(course_id):
            return None
        await self.db[COURSE_COLLECTION].update_one(
            {"_id": ObjectId(course_id)},
            {"$set": update_data},
        )
        doc = await self.db[COURSE_COLLECTION].find_one({"_id": ObjectId(course_id)})
        return _to_course(doc)

    async def delete_course(self, course_id: str) -> bool:
        if not ObjectId.is_valid(course_id):
            return False
        result = await self.db[COURSE_COLLECTION].delete_one({"_id": ObjectId(course_id)})
        return result.deleted_count > 0