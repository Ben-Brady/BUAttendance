from modules.database import users
import pytest

def test_basic():
    user = users.UserData(
        discord_id=1,
        student_id=1234567,
        session_token="TOKEN"
    )
    users.insert(user)
    assert user in users.iter_users()
    assert users.exists(user.discord_id)
    users.delete(user.discord_id)
    assert user not in users.iter_users()

