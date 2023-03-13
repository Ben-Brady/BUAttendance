from . import AttendanceCode
from pickledb import PickleDB


db = PickleDB("./data/codes.json", True, True)


def _iter_codes():
    for data in db.db.values():
        yield AttendanceCode.parse_obj(data)


def link_exists(link: str) -> bool:
    new_code = AttendanceCode.from_link(link)

    for code in _iter_codes():
        if code.progress_code == new_code.progress_code:
            return True

    return False


def insert(code: AttendanceCode):
    db[code.progress_code] = code.dict()


def delete(progress_code: str):
    del db[progress_code]


def exists(progress_code: str) -> bool:
    return db.exists(progress_code)
