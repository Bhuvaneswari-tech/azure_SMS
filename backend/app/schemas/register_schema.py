# from pydantic import BaseModel

# class RegisterRequest(BaseModel):
#     username: str
#     email: str
#     password: str
#     role: str

from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: str = Field(..., min_length=2, max_length=30)