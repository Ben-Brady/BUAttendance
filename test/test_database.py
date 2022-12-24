from modules.database import users
import pytest

def test_users():
    user = users.UserData(
        discord_id=1,
        email="me@example.com",
        session_token="TOKEN",
    )
    users.insert(user)
    assert user in users.iter_users()
    assert users.exists(user.discord_id)
    users.delete(user.discord_id)
    assert user not in users.iter_users()
