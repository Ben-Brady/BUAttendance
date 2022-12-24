from modules.cispr._code import AttendanceCode, SessionCreationError
import pytest

EXAMPLE_CODE = "PoP_L_23_66202646"
EXAMPLE_LINK = "https://cispr.bournemouth.ac.uk/deeplink/qr/TkM4MEx6SXpMMHd2VUc5UVgweGZNak5mTmpZeU1ESTJORFk9"


EXAMPLE_SESSION = AttendanceCode(
    code=EXAMPLE_CODE,
    academic_year="22/23",
    level="Level 4",
    type="L",
    unit_id="4",
    week="23",
)


def test_from_link():
    session = AttendanceCode.from_link(EXAMPLE_LINK)
    assert EXAMPLE_SESSION == session


def test_to_link():
    assert EXAMPLE_SESSION.to_link() == EXAMPLE_LINK


def test_from_link_raises_SessionCreationError():
    with pytest.raises(SessionCreationError):
        AttendanceCode.from_link("https://www.google.com")
    with pytest.raises(SessionCreationError):
        AttendanceCode.from_link(
            "https://cispr.bournemouth.ac.uk/deeplink/qr/TkM4ekx6SXlMMHd2UkVGRVgweGZNakpmTlRVd05qY3h")
