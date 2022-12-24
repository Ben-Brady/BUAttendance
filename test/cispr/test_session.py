from modules import cispr
import pytest



def test_refresh_updates_token ():
    old_token = cispr.get_global_token()
    new_token = cispr.refresh_token(old_token)
    assert old_token != new_token


def test_refresh_raises_SessionExpired():
    with pytest.raises(cispr.CisprSessionExpiredError):
        cispr.refresh_token("asdfasdfasdf")


def test_check_works():
    working_token = cispr.get_global_token()
    assert cispr.check_token(working_token)
    assert cispr.check_token("asdfasdf") == False
