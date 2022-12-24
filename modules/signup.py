from modules import database, cispr
from modules.database import users
import re


class SignupFailure(Exception): pass


def signup_user(user_id: int, email: str, token: str, seminar_group: str):
    EMAIL_REGEX = users.UserData.schema()["properties"]["email"]["pattern"]
    if not re.fullmatch(EMAIL_REGEX, email):
        raise SignupFailure(
            "You provided an invalid email\n"
            "Must be in the format s*STUDENT_CODE*@bournemouth.ac.uk"
        )
    
    SEMINAR_REGEX = users.UserData.schema()["properties"]["seminar_group"]["pattern"]
    if not re.fullmatch(SEMINAR_REGEX, seminar_group):
        raise SignupFailure(
            "You provided an invalid seminar group\n"
            "Must be a single captial letter"
        )
    
    if not cispr.check_token(token):
        raise SignupFailure("The Session Token you provided didn't work")
    
    try:
        users.UserData.schema_json()
        user = users.UserData(
            discord_id=user_id,
            email=email,
            session_token=token,
            seminar_group=seminar_group,
            automatic_attendance=False,
        )
    except Exception as e:
        raise SignupFailure(f"Unexpected Error: {str(e)}")

    
    users.insert(user)
