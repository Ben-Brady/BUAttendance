from . import AttendanceCode
from pickledb import PickleDB


db = PickleDB("./data/codes.json", True, True)


def insert(session: AttendanceCode):
    db.set(session.code, session.dict())


def delete(code: str):
    db.rem(code)


def exists(code: str) -> bool:
    return db.exists(code)
