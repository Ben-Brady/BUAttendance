from modules import students
from typing import Iterable
from pydantic import BaseModel, Field
from pickledb import PickleDB


db = PickleDB("./data/users.json", True, True)


class UserData(BaseModel):
    discord_id: int = Field(...)
    student_id: int = Field(...)
    session_token: str = Field(...)

    @property
    def email(self):
        return f"s{self.student_id}@bournemouth.ac.uk"



def insert(user: UserData):
    db.set(str(user.discord_id), user.dict())


def update(
    discord_id: int, *,
    student_id: int | None = None,
    session_token: str | None = None,
):
    if not exists(discord_id):
        raise KeyError

    data = db.get(id)
    user = UserData.parse_obj(data)
    user.student_id = student_id or user.student_id
    user.session_token = session_token or user.session_token

    db.set(id, user.dict())


def delete(discord_id: int):
    db.rem(str(discord_id))


def iter_users() -> Iterable[UserData]:
    for data in db.db.values():
        yield UserData.parse_obj(data)


def iter_seminar_group(seminar_group: str) -> Iterable[UserData]:
    for data in db.db.values():
        user = UserData.parse_obj(data)
        student = students.from_id(user.student_id)
        if student and student.seminar_group == seminar_group:
            yield user


def exists(discord_id: int) -> bool:
    return db.exists(str(discord_id))
