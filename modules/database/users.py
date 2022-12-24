from typing import Iterable
from pydantic import BaseModel
from pickledb import PickleDB


db = PickleDB("./data/users.json", True, True)


class UserData(BaseModel):
    discord_id: int
    email: str
    session_token: str


def insert(user: UserData):
    db.set(str(user.discord_id), user.dict())


def update(
        discord_id: int,
        *,
        token: str | None = None,
        email: str | None = None,
        ):
    if not exists(discord_id):
        raise KeyError

    data = db.get(id)
    user = UserData.parse_obj(data)
    user.session_token = token or user.session_token
    user.email = email or user.email
    
    db.set(id, user.dict())


def delete(discord_id: int):
    db.rem(str(discord_id))


def iter_users() -> Iterable[UserData]:
    for data in db.db.values():
        yield UserData.parse_obj(data)


def exists(discord_id: int) -> bool:
    return db.exists(str(discord_id))
