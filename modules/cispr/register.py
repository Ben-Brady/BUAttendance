from . import get_global_token, AttendanceCode
import requests


class AttendanceFailure(Exception):
    pass


def register_attendance(session: AttendanceCode, email: str):
    r = requests.post(
        url="https://cispr.bournemouth.ac.uk/study-progress/submit",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        cookies={
            "cispr_session": get_global_token(),
        },
        data={
            "_token": "Q7F6ItxUsLKBGxX35jOzFjDflYVeJJjRDapgxkV5",
            "email_address": email,
            "level": session.level,
            "unit_id": session.unit_id,
            "session_ay": session.academic_year,
            "session_week": session.week,
            "session_type": session.type,
            "attendance_code": session.code,
            "disclaimer": "on",
        }
    )

    if r.status_code != 200:
        raise AttendanceFailure
