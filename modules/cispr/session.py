import requests
from pathlib import Path


TOKEN_STORE = Path("./data/cispr_session")
KNOWN_TOKEN = "eyJpdiI6Im9EL0gxMWpabjJYVEVlNzNPT0w1NEE9PSIsInZhbHVlIjoiaWhoQnNCK1dwNFhtbUFubHZPLzJFSy9rWWZCcVZ0TDZPcVZxdkdBelhaTVlLTU1ZajRuVW5pQ3NuU0J1ZVREWkpkbU9MT2UxZHkzdXpUV3V1azBRODlZMk16QXZEQTlrTzA5QUxoeTloZlQxV1N0WTQ3NWhnZWhYVGk2eUhLQlIiLCJtYWMiOiI0YWRmZmE1NDkzNzU1NDY5YjdhNGRlYmQ5MmMzMzZmMjU0NzIyNDc2MmUxZGVkZDRiNjZhOTkwNDRkM2U4NTk3IiwidGFnIjoiIn0%3D"


class CisprSessionExpiredError(Exception):
    pass


def get_global_token() -> str:
    if not TOKEN_STORE.exists():
        return KNOWN_TOKEN

    token = TOKEN_STORE.read_text()
    if token != "":
        return token
    else:
        return KNOWN_TOKEN


def set_global_token(new_token: str):
    TOKEN_STORE.write_text(new_token)


def refresh_token(token: str) -> str:
    r = requests.get(
        url="https://cispr.bournemouth.ac.uk/study-progress",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
        },
        cookies={
            "cispr_session": token
        },
        allow_redirects=False
    )

    new_token = r.cookies.get("cispr_session")
    if new_token == None:
        raise CisprSessionExpiredError

    return new_token


def check_token(token: str) -> bool:
    "Checks if a cirsp token functional"
    try:
        refresh_token(token)
    except CisprSessionExpiredError:
        return False
    else:
        return True
