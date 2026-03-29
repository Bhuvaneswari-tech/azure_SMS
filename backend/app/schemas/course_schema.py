# from pydantic import BaseModel

# class CourseBase(BaseModel):
#     title: str
#     description: str

# class CourseCreate(CourseBase):
#     pass

# class Course(CourseBase):
#     id: int
#     class Config:
#         orm_mode = True

from pydantic import BaseModel, ConfigDict, Field


class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: str | None = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None


class Course(CourseBase):
    id: str
    model_config = ConfigDict(from_attributes=True)