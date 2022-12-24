from . import AttendanceCode
from modules import cispr, database
import asyncio
import random


class AttendanceFailure(Exception):
    pass


async def attend_all_users(code_info: AttendanceCode):
    all_users = database.users.iter_users()
    coros = [_attend_user(code_info, user) for user in all_users]
    await asyncio.gather(*coros)


async def attend_seminar_group(seminar_group: str, code_info: AttendanceCode):
    raise NotImplementedError


async def _attend_user(code_info: AttendanceCode, user: database.UserData):
    delay_time = random.random() * 300
    await asyncio.sleep(delay_time)
    cispr.register_attendance(code_info, user.email)
