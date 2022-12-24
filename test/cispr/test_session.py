from modules import cispr
import pytest

@pytest.fixture()
def reset_token():
    token = cispr.get_token()
    yield
    cispr.set_token(token)



def test_refresh_update():
    old_token = cispr.get_token()
    cispr.refresh_token()
    new_token = cispr.get_token()
    assert old_token != new_token


def test_refresh_asserts(reset_token):
    cispr.set_token("")
    with pytest.raises(cispr.CisprSessionExpiredError):
        cispr.refresh_token()
