from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.enrollment_repository import EnrollmentRepository
from app.schemas import enrollment_schema


class EnrollmentService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = EnrollmentRepository(db)

    async def create_enrollment(self, enrollment: enrollment_schema.EnrollmentCreate):
        return await self.repo.create_enrollment(enrollment.model_dump())

    async def get_enrollment(self, enrollment_id: str):
        return await self.repo.get_enrollment(enrollment_id)

    async def list_enrollments(self):
        return await self.repo.list_enrollments()

    async def delete_enrollment(self, enrollment_id: str) -> bool:
        return await self.repo.delete_enrollment(enrollment_id)