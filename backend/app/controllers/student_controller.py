from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.database import get_database
from app.schemas import student_schema
from app.services.student_service import StudentService

router = APIRouter()


def get_student_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> StudentService:
    return StudentService(db)


@router.post("/students/", response_model=student_schema.Student, status_code=status.HTTP_201_CREATED)
async def create_student(
    student: student_schema.StudentCreate,
    service: StudentService = Depends(get_student_service),
):
    return await service.create_student(student)


@router.get("/students/{student_id}", response_model=student_schema.Student)
async def get_student(
    student_id: str,
    service: StudentService = Depends(get_student_service),
):
    db_student = await service.get_student(student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.get("/students/", response_model=list[student_schema.Student])
async def list_students(service: StudentService = Depends(get_student_service)):
    return await service.list_students()