from modules import discord, students, cispr, logging
from modules.config import _Config


logging.load()
students.load()

if not cispr.check_token(cispr.get_global_token()):
    print("Global CISPR Token has expired")


config = _Config()
discord.start_bot(config.token)
