from datetime import timedelta

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from app.dependencies import auth
from app.models.database import get_database
from app.models.role import ROLE_COLLECTION
from app.models.user import USER_COLLECTION
from app.schemas.register_schema import RegisterRequest
from app.schemas.token_schema import Token

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login", response_model=Token, summary="Login and get JWT token")
async def login_for_access_token(
    payload: LoginRequest = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    user = await db[USER_COLLECTION].find_one({"email": payload.email})
    if not user or not auth.verify_password(payload.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    role_name = None
    role_id = user.get("role_id")
    if role_id:
        role_doc = None
        if isinstance(role_id, str) and ObjectId.is_valid(role_id):
            role_doc = await db[ROLE_COLLECTION].find_one({"_id": ObjectId(role_id)})
        else:
            role_doc = await db[ROLE_COLLECTION].find_one({"name": str(role_id)})
        if role_doc:
            role_name = role_doc.get("name")

    access_token = auth.create_access_token(
        data={"sub": user.get("username"), "role": role_name},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_name,
        "user_id": str(user["_id"]),
    }


@router.post("/register", response_model=Token, summary="Register user and get JWT token")
async def register_user(
    payload: RegisterRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    existing_user = await db[USER_COLLECTION].find_one(
        {"$or": [{"username": payload.username}, {"email": payload.email}]}
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    role = await db[ROLE_COLLECTION].find_one({"name": payload.role})
    if not role:
        insert_res = await db[ROLE_COLLECTION].insert_one({"name": payload.role})
        role = await db[ROLE_COLLECTION].find_one({"_id": insert_res.inserted_id})

    user_doc = {
        "username": payload.username,
        "email": payload.email,
        "hashed_password": auth.hash_password(payload.password),
        "role_id": str(role["_id"]),
        "disabled": 0,
    }
    inserted = await db[USER_COLLECTION].insert_one(user_doc)

    access_token = auth.create_access_token(
        data={"sub": payload.username, "role": role.get("name")},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role.get("name"),
        "user_id": str(inserted.inserted_id),
    }


@router.get("/me")
async def read_users_me(current_user: dict = Depends(auth.get_current_active_user)):
    return current_user


@router.get("/admin-only")
async def admin_only(current_user: dict = Depends(auth.require_role("admin"))):
    return {"msg": f"Hello, {current_user['username']}. You are an admin."}


@router.get("/user-only")
async def user_only(current_user: dict = Depends(auth.require_role("student"))):
    return {"msg": f"Hello, {current_user['username']}. You are a student."}