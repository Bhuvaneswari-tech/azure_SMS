from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.enrollment import ENROLLMENT_COLLECTION


def _to_enrollment(doc: dict | None):
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "student_id": doc["student_id"],
        "course_id": doc["course_id"],
    }


class EnrollmentRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_enrollment(self, data: dict):
        result = await self.db[ENROLLMENT_COLLECTION].insert_one(data)
        doc = await self.db[ENROLLMENT_COLLECTION].find_one({"_id": result.inserted_id})
        return _to_enrollment(doc)

    async def get_enrollment(self, enrollment_id: str):
        if not ObjectId.is_valid(enrollment_id):
            return None
        doc = await self.db[ENROLLMENT_COLLECTION].find_one({"_id": ObjectId(enrollment_id)})
        return _to_enrollment(doc)

    async def list_enrollments(self):
        docs = await self.db[ENROLLMENT_COLLECTION].find().to_list(length=1000)
        return [_to_enrollment(doc) for doc in docs]

    async def delete_enrollment(self, enrollment_id: str) -> bool:
        if not ObjectId.is_valid(enrollment_id):
            return False
        result = await self.db[ENROLLMENT_COLLECTION].delete_one({"_id": ObjectId(enrollment_id)})
        return result.deleted_count > 0