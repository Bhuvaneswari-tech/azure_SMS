import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.controllers.webhook_notify import notify_webhook
from app.models.database import get_database
from app.schemas import course_schema
from app.services.course_service import CourseService

router = APIRouter()


def get_course_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> CourseService:
    return CourseService(db)


@router.post("/courses/", response_model=course_schema.Course, status_code=status.HTTP_201_CREATED)
async def create_course(
    course: course_schema.CourseCreate,
    service: CourseService = Depends(get_course_service),
):
    created = await service.create_course(course)
    asyncio.create_task(notify_webhook("course_create", "success", {"id": created["id"]}))
    return created


@router.get("/courses/{course_id}", response_model=course_schema.Course)
async def get_course(
    course_id: str,
    service: CourseService = Depends(get_course_service),
):
    db_course = await service.get_course(course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.get("/courses/", response_model=list[course_schema.Course])
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    service: CourseService = Depends(get_course_service),
):
    courses = await service.list_courses()
    return courses[skip : skip + limit]


@router.put("/courses/{course_id}", response_model=course_schema.Course)
async def update_course(
    course_id: str,
    course: course_schema.CourseUpdate,
    service: CourseService = Depends(get_course_service),
):
    updated = await service.update_course(course_id, course)
    if updated is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated


@router.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: str,
    service: CourseService = Depends(get_course_service),
):
    deleted = await service.delete_course(course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    return None