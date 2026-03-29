from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.course_repository import CourseRepository
from app.schemas import course_schema


class CourseService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repo = CourseRepository(db)

    async def create_course(self, course: course_schema.CourseCreate):
        return await self.repo.create_course(course.model_dump())

    async def get_course(self, course_id: str):
        return await self.repo.get_course(course_id)

    async def list_courses(self):
        return await self.repo.list_courses()

    async def update_course(self, course_id: str, course: course_schema.CourseUpdate):
        return await self.repo.update_course(course_id, course.model_dump(exclude_none=True))

    async def delete_course(self, course_id: str) -> bool:
        return await self.repo.delete_course(course_id)