from logging.config import fileConfig

fileConfig("./logging.conf")

from . import config, database, qrcode
from . import cispr
from . import discord
from . import commands