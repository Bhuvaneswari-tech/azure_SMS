import pytest
from app.models.user import User

def test_create_user():
    user = User(username="testuser", full_name="Test User", email="test@example.com", hashed_password="hashed", role_id=1)
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_user_disabled_default():
    user = User(username="testuser2", full_name="Test User2", email="test2@example.com", hashed_password="hashed2", role_id=2)
    assert user.disabled == 0
