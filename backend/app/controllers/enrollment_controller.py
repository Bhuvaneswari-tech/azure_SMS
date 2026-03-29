from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.database import get_database
from app.schemas import enrollment_schema
from app.services.enrollment_service import EnrollmentService

router = APIRouter()


def get_enrollment_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> EnrollmentService:
    return EnrollmentService(db)


@router.post("/enrollments/", response_model=enrollment_schema.Enrollment, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment: enrollment_schema.EnrollmentCreate,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return await service.create_enrollment(enrollment)


@router.get("/enrollments/{enrollment_id}", response_model=enrollment_schema.Enrollment)
async def get_enrollment(
    enrollment_id: str,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    db_enrollment = await service.get_enrollment(enrollment_id)
    if db_enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return db_enrollment


@router.get("/enrollments/", response_model=list[enrollment_schema.Enrollment])
async def list_enrollments(service: EnrollmentService = Depends(get_enrollment_service)):
    return await service.list_enrollments()


@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(
    enrollment_id: str,
    service: EnrollmentService = Depends(get_enrollment_service),
):
    deleted = await service.delete_enrollment(enrollment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return None