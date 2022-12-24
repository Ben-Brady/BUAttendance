from modules.cispr import get_account_name_and_id, get_global_token
import pytest

EXAMPLE_CODE = "PoP_L_23_66202646"
EXAMPLE_LINK = "https://cispr.bournemouth.ac.uk/deeplink/qr/TkM4MEx6SXpMMHd2VUc5UVgweGZNak5mTmpZeU1ESTJORFk9"


def test_from_token():
    token = get_global_token()
    name, id = get_account_name_and_id(token)
    assert name == "Ben Brady"
    assert id == 5524995
