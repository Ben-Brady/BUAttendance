from modules.config import Config
from modules.cispr._code import AttendanceCode
from discord import Client
from discord.abc import GuildChannel


config = Config()


class SendAttedanceCodeError(Exception):
    pass


async def send_attendance_code(client: Client, info: AttendanceCode) -> bool:
    channel = client.get_channel(config.attendence_channel)
    if not isinstance(channel, GuildChannel):
        raise Exception

    if channel:
        await channel.send("")
