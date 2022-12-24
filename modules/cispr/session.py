import requests
from pathlib import Path


TOKEN_STORE = Path("./data/cispr_session")
KNOWN_TOKEN = "eyJpdiI6Im9EL0gxMWpabjJYVEVlNzNPT0w1NEE9PSIsInZhbHVlIjoiaWhoQnNCK1dwNFhtbUFubHZPLzJFSy9rWWZCcVZ0TDZPcVZxdkdBelhaTVlLTU1ZajRuVW5pQ3NuU0J1ZVREWkpkbU9MT2UxZHkzdXpUV3V1azBRODlZMk16QXZEQTlrTzA5QUxoeTloZlQxV1N0WTQ3NWhnZWhYVGk2eUhLQlIiLCJtYWMiOiI0YWRmZmE1NDkzNzU1NDY5YjdhNGRlYmQ5MmMzMzZmMjU0NzIyNDc2MmUxZGVkZDRiNjZhOTkwNDRkM2U4NTk3IiwidGFnIjoiIn0%3D"


def init_token() -> str:
    if not TOKEN_STORE.exists():
        return KNOWN_TOKEN
    
    token = TOKEN_STORE.read_text()
    if token != "":
        return token
    else:
        return KNOWN_TOKEN


token = init_token()


class CisprSessionExpiredError(Exception):
    pass



def get_token() -> str:
    return token



def set_token(new_token: str):
    global token
    token = new_token
    TOKEN_STORE.write_text(token)



def refresh_token():
    r = requests.get(
        url="https://cispr.bournemouth.ac.uk/study-progress",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
        },
        cookies={
            "cispr_session": get_token()
        }
    )

    token = r.cookies.get("cispr_session")
    if token == None:
        raise CisprSessionExpiredError

    set_token(token)
