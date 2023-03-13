from modules import database, cispr
from modules.database import users
import re


class SignupFailure(Exception):
    pass


def signup_user(discord_id: int, student_id: int, token: str):
    ID_REGEX = r"\d{7}"
    if not re.fullmatch(ID_REGEX, str(student_id)):
        raise SignupFailure(
            "You provided an invalid seminar group\n"
            "Must be a single captial letter"
        )

    if not cispr.check_token(token):
        raise SignupFailure("The Session Token you provided didn't work")

    try:
        users.UserData.schema_json()
        user = users.UserData(
            discord_id=discord_id,
            student_id=student_id,
            session_token=token,
        )
    except Exception as e:
        raise SignupFailure(f"Unexpected Error: {str(e)}")

    users.insert(user)
