class Response(Exception):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg

from .attendace import send_attendance_code, SendAttedanceCodeError
from .utils import download_image