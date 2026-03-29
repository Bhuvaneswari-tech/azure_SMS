# from .database import Base
# from sqlalchemy import Column, Integer

# class Enrollment(Base):
#     __tablename__ = "enrollments"
#     id = Column(Integer, primary_key=True, index=True)
#     student_id = Column(Integer, index=True)
#     course_id = Column(Integer, index=True)

from typing import TypedDict

ENROLLMENT_COLLECTION = "enrollments"

class EnrollmentDocument(TypedDict):
    student_id: str
    course_id: str