import pytest
from app.models.course import Course

def test_create_course():
    course = Course(title="Math", description="Mathematics course")
    assert course.title == "Math"
    assert course.description == "Mathematics course"

def test_course_id_default():
    course = Course(title="Science", description="Science course")
    assert hasattr(course, "id")
