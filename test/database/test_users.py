from modules.database import users
import pytest

def test_basic():
    user = users.UserData(
        discord_id=1,
        email="s1234567@bournemouth.ac.uk",
        session_token="TOKEN",
        seminar_group="F"
    )
    users.insert(user)
    assert user in users.iter_users()
    assert users.exists(user.discord_id)
    users.delete(user.discord_id)
    assert user not in users.iter_users()


def test_iter_seminar_group():
    user_a = users.UserData(
        discord_id=1,
        email="s1234567@bournemouth.ac.uk",
        session_token="TOKEN",
        seminar_group="A"
    )
    user_b = users.UserData(
        discord_id=2,
        email="s2345678@bournemouth.ac.uk",
        session_token="TOKEN",
        seminar_group="B"
    )
    
    users.insert(user_a)
    users.insert(user_b)
    assert list(users.iter_seminar_group("A")) == [user_a]
    assert list(users.iter_seminar_group("B")) == [user_b]
