# from pydantic import BaseModel


# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str


# class User(BaseModel):
#     id: int
#     username: str
#     email: str
#     role_id: int
#     disabled: int = 0
#     class Config:
#         orm_mode = True

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=100)
    role_id: str | None = None
    disabled: int = 0


class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: str | None = None
    role_id: str | None = None
    disabled: int = 0

    model_config = ConfigDict(from_attributes=True)