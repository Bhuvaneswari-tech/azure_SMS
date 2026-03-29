from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.database import get_database
from app.schemas import role_schema
from app.services.role_service import RoleService

router = APIRouter()


def get_role_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> RoleService:
    return RoleService(db)


@router.post("/roles/", response_model=role_schema.Role, status_code=status.HTTP_201_CREATED)
async def create_role(
    role: role_schema.RoleCreate,
    service: RoleService = Depends(get_role_service),
):
    existing = await service.get_role_by_name(role.name)
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    return await service.create_role(role)


@router.get("/roles/{role_id}", response_model=role_schema.Role)
async def get_role(
    role_id: str,
    service: RoleService = Depends(get_role_service),
):
    db_role = await service.get_role(role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.get("/roles/", response_model=list[role_schema.Role])
async def list_roles(service: RoleService = Depends(get_role_service)):
    return await service.list_roles()


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: str,
    service: RoleService = Depends(get_role_service),
):
    deleted = await service.delete_role(role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return None