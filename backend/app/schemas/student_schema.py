# from pydantic import BaseModel

# class StudentBase(BaseModel):
#     name: str
#     email: str

# class StudentCreate(StudentBase):
#     pass

# class Student(StudentBase):
#     id: int
#     class Config:
#         orm_mode = True

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class Student(StudentBase):
    id: str
    model_config = ConfigDict(from_attributes=True)