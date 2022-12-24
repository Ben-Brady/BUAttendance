from modules import qrcode
import pytest


def assert_qr_code(filepath: str, text: str):
    with open(filepath, "rb") as f:
        data = f.read()
    
    value = qrcode.read(data)
    assert value == text


def test_perfect_qrcode():
    assert_qr_code("./test/perfect_qr.jpg", "http://q-r.to/bapfTn")


@pytest.mark.skip()
def test_irl_qrcode():
    assert_qr_code("./test/easy_qr.png", "http://q-r.to/bapfTn")


@pytest.mark.skip()
def test_hard_qrcode():
    assert_qr_code("./test/irl_qr.jpg", "http://q-r.to/bapfTn")
