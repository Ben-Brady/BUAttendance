from . import bot
from modules.config import _Config
from modules.cispr._code import AttendanceCode
from discord import Client
from discord import TextChannel


config = _Config()


class SendAttedanceCodeError(Exception):
    pass

UNIT_LOOKUP = {
    "4": "PRINCIPLES OF PROGRAMMING",
    "2": "COMPUTER FUNDAMENTALS",
    "3": "DATA & DATABASES",
    
    "5": "APPLICATION OF PROGRAMMING PRINCIPLES",
    "6": "BUSINESS SYSTEMS ANALYSIS AND DESIGN",
    "7": "NETWORKS AND CYBER SECURITY",
    
    "1": "INDUCTION",
    "95": "GENERAL COMPUTING SESSIONS",
}

async def send_attendance_code(code: AttendanceCode):
    channel = bot.get_channel(config.attendence_channel)
    if not isinstance(channel, TextChannel):
        raise SendAttedanceCodeError("Unable find channel based on ID")
    

    if not channel.can_send():
        raise SendAttedanceCodeError("Unable to send message in announcement channel")
    
    course_name = UNIT_LOOKUP.get(code.unit_id, "Unknown Course")
    await channel.send(
        "<@1078242231699394570>\n"
        f"**L4 | Week {code.week}**\n"
        f"**{course_name}**\n"
        f"{code.progress_code}\n"
        "\n"
        f"{code.link}\n"
    )
