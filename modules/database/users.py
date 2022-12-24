from typing import Iterable
from pydantic import BaseModel, Field
from pickledb import PickleDB


db = PickleDB("./data/users.json", True, True)


class UserData(BaseModel):
    discord_id: int = Field(...)
    email: str = Field(..., regex="^s[0-9]{7}@bournemouth.ac.uk$")
    session_token: str = Field(...)
    seminar_group: str = Field(..., max_length=1, regex="^[A-Z]$")
    automatic_attendance: bool = Field(default=False)


def insert(user: UserData):
    db.set(str(user.discord_id), user.dict())


def update(
        discord_id: int,
        *,
        email: str | None = None,
        session_token: str | None = None,
        seminar_group: str | None = None,
        automatic_attendance: bool | None = None,
):
    if not exists(discord_id):
        raise KeyError

    data = db.get(id)
    user = UserData.parse_obj(data)
    user.email = email or user.email
    user.session_token = session_token or user.session_token
    user.seminar_group = seminar_group or user.seminar_group
    user.automatic_attendance = automatic_attendance or user.automatic_attendance

    db.set(id, user.dict())


def delete(discord_id: int):
    db.rem(str(discord_id))


def iter_users() -> Iterable[UserData]:
    for data in db.db.values():
        yield UserData.parse_obj(data)


def iter_seminar_group(seminar_group: str) -> Iterable[UserData]:
    for data in db.db.values():
        user = UserData.parse_obj(data)
        if user.seminar_group == seminar_group:
            yield user


def exists(discord_id: int) -> bool:
    return db.exists(str(discord_id))
