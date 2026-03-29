import pytest
from app.models.role import Role

def test_create_role():
    role = Role(name="admin")
    assert role.name == "admin"

def test_role_id_default():
    role = Role(name="user")
    assert hasattr(role, "id")
