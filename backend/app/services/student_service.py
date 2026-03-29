from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.student_repository import StudentRepository
from app.schemas import student_schema


class StudentService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = StudentRepository(db)

    async def create_student(self, student: student_schema.StudentCreate):
        return await self.repo.create_student(student.model_dump())

    async def get_student(self, student_id: str):
        return await self.repo.get_student(student_id)

    async def list_students(self):
        return await self.repo.list_students()

    async def update_student(self, student_id: str, data: student_schema.StudentUpdate):
        return await self.repo.update_student(student_id, data.model_dump(exclude_none=True))

    async def delete_student(self, student_id: str) -> bool:
        return await self.repo.delete_student(student_id)