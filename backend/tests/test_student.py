import pytest
from app.models.student import Student

def test_create_student():
    student = Student(name="Student1", email="student1@example.com")
    assert student.name == "Student1"
    assert student.email == "student1@example.com"

def test_student_id_default():
    student = Student(name="Student2", email="student2@example.com")
    assert hasattr(student, "id")
