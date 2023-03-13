from . import get_global_token, AttendanceCode
import requests


class AttendanceFailure(Exception):
    pass


def register_attendance(code: AttendanceCode, email: str):
    r = requests.post(
        url="https://cispr.bournemouth.ac.uk/study-progress/submit",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        cookies={
            "cispr_session": get_global_token(),
            "XSRF-TOKEN": get_global_token(),
        },
        data={
            "_token": "ipp7kIdp3Hd4OoPEekjHeNgsHNq01GPIGuPUFNj3",
            "email_address": email,
            "level": code.level,
            "unit_id": code.unit_id,
            "session_ay": code.academic_year,
            "session_week": code.week,
            "session_type": code.type,
            "attendance_code": code.progress_code,
            "disclaimer": "on",
        }
    )

    if r.status_code == 302:
        return
    elif r.status_code == 419:
        raise AttendanceFailure("Attendance Code Expired")
    else:
        raise AttendanceFailure(f"Unknown Response: {r.status_code}")
