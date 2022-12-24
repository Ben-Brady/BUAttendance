from . import get_token, CisprSessionExpiredError
import logging
from base64 import b64encode
import requests
from pydantic import BaseModel, Field
import bs4


class SessionCreationError(Exception):
    pass


class AttendanceCode(BaseModel):
    code: str = Field(...,
                      regex=r"^[A-Za-z0-9]{1,5}_[LS]_[0-9]{1,2}_[0-9]{8}$")
    week: str = Field(..., regex=r"^[0-9]+$")
    academic_year: str = Field(..., regex=r"^[0-9]{2}\/[0-9]{2}$")
    level: str = Field(..., regex=r"^Level [04567]$")
    type: str = Field(..., regex=r"^(L|S)$")
    unit_id: str = Field(..., regex=r"^[0-9]$")

    def to_link(self):
        data = "4/{unit_id}/{week}/{type}/{code}".format(
            unit_id=self.unit_id,
            week=self.week,
            type=self.type,
            code=self.code
        )
        encoded_data = b64encode(b64encode(data.encode())).decode()
        return f"https://cispr.bournemouth.ac.uk/deeplink/qr/{encoded_data}"

    @staticmethod
    def from_link(link: str):
        try:
            return parse_link(link)
        except CisprSessionExpiredError:
            logging.error(
                "The CISPR Session has Expired, you need to update the token")
            raise
        except Exception as e:
            logging.info(f"Could not prase link: {link} due to {e}")
            raise SessionCreationError


def parse_link(link: str) -> AttendanceCode:
    r = requests.get(
        url=link,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
        },
        cookies={
            "cispr_session": get_token(),
        },
    )

    soup = bs4.BeautifulSoup(r.text, "html")
    form = soup.find("form")
    if form == None:
        raise CisprSessionExpiredError

    data = {}
    for elem in form.find_all("input"):  # type: ignore
        if elem.attrs.get("type") == "radio" and "checked" not in elem.attrs:
            continue

        key = elem.attrs["name"]
        value = elem.attrs.get("value")
        data[key] = value

    for select_elem in form.find_all("select"):  # type: ignore
        key, value = parse_select(select_elem)
        data[key] = value

    data["disclaimer"] = "on"

    return AttendanceCode(
        code=data["attendance_code"],
        week=data["session_week"],
        academic_year=data["session_ay"],
        level=data["level"],
        unit_id=data["unit_id"],
        type=data["session_type"],
    )


def parse_select(select_elem: bs4.Tag) -> tuple[str, str]:
    key = select_elem.attrs["name"]

    value = None
    for child in select_elem.find_all("option"):
        if "selected" in child.attrs and "disabled" not in child.attrs:
            value = child.attrs["value"]
            break

    if value is None:
        raise ValueError(f"{key} could not be extracted")

    return key, value
