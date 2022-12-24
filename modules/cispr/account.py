from . import get_global_token, check_token, CisprSessionExpiredError
import requests
import bs4
import re


def get_account_name_and_id(token: str) -> tuple[str, int]:
    r = requests.get(
        url="https://cispr.bournemouth.ac.uk/study-progress",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
        },
        cookies={
            "cispr_session": token,
        }
    )

    soup = bs4.BeautifulSoup(r.text, features="html")
    name_elem = soup.find(
        "div", attrs={"class": "text-base font-medium leading-none mb-1"})
    if not name_elem:
        raise CisprSessionExpiredError("Could not extract data from page")

    id = from_regex(r"\d+", name_elem.text)
    name = from_regex(r"[a-zA-Z ]+(?= \()", name_elem.text)

    return name, int(id)


def from_regex(pattern: str, text: str) -> str:
    match = re.search(pattern, text)
    if match == None:
        raise CisprSessionExpiredError("Could not extract data from page")
    else:
        return match.group()