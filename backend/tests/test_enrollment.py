import pytest
from app.models.enrollment import Enrollment

def test_create_enrollment():
    enrollment = Enrollment(student_id=1, course_id=2)
    assert enrollment.student_id == 1
    assert enrollment.course_id == 2

def test_enrollment_id_default():
    enrollment = Enrollment(student_id=3, course_id=4)
    assert hasattr(enrollment, "id")
