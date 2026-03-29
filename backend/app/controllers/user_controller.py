from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.database import get_database
from app.schemas import user_schema
from app.services.user_service import UserService

router = APIRouter()


def get_user_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserService:
    return UserService(db)


@router.post("/users/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: user_schema.UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.create_user(user)


@router.get("/users/{user_id}", response_model=user_schema.User)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    db_user = await service.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=list[user_schema.User])
async def list_users(service: UserService = Depends(get_user_service)):
    return await service.list_users()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None