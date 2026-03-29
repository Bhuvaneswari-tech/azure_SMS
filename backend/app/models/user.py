# from .database import Base
# from sqlalchemy import Column, Integer, String

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     full_name = Column(String)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     role_id = Column(Integer, index=True)
#     disabled = Column(Integer, default=0, nullable=False)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         if 'disabled' not in kwargs or kwargs['disabled'] is None:
#             self.disabled = 0
            

# # What does it do?

# # Checks if disabled is missing or set to None in the constructor arguments.
# # If so, sets self.disabled = 0 so the object behaves as expected in Python code and tests.

from typing import TypedDict, NotRequired

USER_COLLECTION = "users"

class UserDocument(TypedDict):
    username: str
    full_name: str
    email: str
    hashed_password: str
    role_id: str
    disabled: NotRequired[int]