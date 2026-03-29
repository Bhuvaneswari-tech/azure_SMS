
# # --- Password Hashing Utilities ---
# from passlib.context import CryptContext
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# # --- JWT Utilities ---
# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt

# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # --- User Lookup ---
# from app.models.user import User
# from app.models.role import Role
# from app.models.database import get_db
# from sqlalchemy.orm import Session

# def get_user(db: Session, username: str):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         return None
#     role = db.query(Role).filter(Role.id == user.role_id).first()
#     role_name = role.name if role else None
#     return {
#         "username": user.username,
#         "full_name": getattr(user, "full_name", None),
#         "role": role_name,
#         "disabled": bool(getattr(user, "disabled", False)),
#         "hashed_password": user.hashed_password
#     }

# def authenticate_user(db: Session, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user["hashed_password"]):
#         return False
#     return user

# # --- FastAPI Auth Dependencies ---
# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# bearer_scheme = HTTPBearer()

# def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         role: str = payload.get("role")
#         if username is None or role is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=username)
#     if user is None:
#         raise credentials_exception
#     return user

# def get_current_active_user(current_user: dict = Depends(get_current_user)):
#     if current_user["disabled"]:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# def require_role(role: str):
#     def role_checker(current_user: dict = Depends(get_current_active_user)):
#         if current_user["role"] != role:
#             raise HTTPException(status_code=403, detail="Not enough permissions")
#         return current_user
#     return role_checker

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_user(db: Session, username: str):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         return None
#     role = db.query(Role).filter(Role.id == user.role_id).first()
#     role_name = role.name if role else None
#     return {
#         "username": user.username,
#         "role": role_name,
#         "disabled": bool(getattr(user, "disabled", False)),
#         "hashed_password": user.hashed_password
#     }

# def authenticate_user(db: Session, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         role: str = payload.get("role")
#         if username is None or role is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=username)
#     if user is None:
#         raise credentials_exception
#     return user

# def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user["disabled"]:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# def require_role(role: str):
#     def role_checker(current_user: dict = Depends(get_current_active_user)):
#         if current_user["role"] != role:
#             raise HTTPException(status_code=403, detail="Not enough permissions")
#         return current_user
#     return role_checker

from datetime import datetime, timedelta
from typing import Optional, Any
import os

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.context import CryptContext

from app.models.database import get_database
from app.models.user import USER_COLLECTION
from app.models.role import ROLE_COLLECTION


# --- Security / JWT Config ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


# --- Password Hashing ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# --- JWT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- Mongo User Lookup ---
async def get_user(db: AsyncIOMotorDatabase, username: str) -> dict[str, Any] | None:
    user = await db[USER_COLLECTION].find_one({"username": username})
    if not user:
        return None

    role_name = None
    role_id = user.get("role_id")

    if role_id:
        role = None
        if isinstance(role_id, str) and ObjectId.is_valid(role_id):
            role = await db[ROLE_COLLECTION].find_one({"_id": ObjectId(role_id)})
        else:
            role = await db[ROLE_COLLECTION].find_one({"name": str(role_id)})

        if role:
            role_name = role.get("name")

    return {
        "username": user.get("username"),
        "full_name": user.get("full_name"),
        "role": role_name,
        "disabled": bool(user.get("disabled", 0)),
        "hashed_password": user.get("hashed_password", ""),
    }


async def authenticate_user(db: AsyncIOMotorDatabase, username: str, password: str) -> dict[str, Any] | bool:
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user


# --- FastAPI Dependencies ---
async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(role: str):
    async def role_checker(current_user: dict[str, Any] = Depends(get_current_active_user)) -> dict[str, Any]:
        if current_user["role"] != role:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user

    return role_checker