# from pydantic import BaseModel

# class RoleBase(BaseModel):
#     name: str

# class RoleCreate(RoleBase):
#     pass

# class Role(RoleBase):
#     id: int
#     class Config:
#         orm_mode = True

from pydantic import BaseModel, ConfigDict, Field


class RoleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)


class Role(RoleBase):
    id: str
    model_config = ConfigDict(from_attributes=True)