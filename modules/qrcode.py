import io
from PIL import Image
import zbarlight

class InvalidQRCode(Exception): pass


def read(data: bytes) -> str:
    buf = io.BytesIO(data)
    image = Image.open(buf)
    codes = zbarlight.scan_codes(['qrcode'], image)

    if len(codes) != 1:
        raise InvalidQRCode

    text = codes[0]
    return text.decode()
