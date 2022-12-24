from modules import cispr, config, commands
import logging
import discord
from discord import Permissions
from discord.ext import tasks


intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)
bot_config = config.Config()


@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')
    task_refresh_token.start()


@tasks.loop(hours=1)
async def task_refresh_token():
    cispr.refresh_token()


bot.slash_command(
    name="set_channel",
    desciption="",
    guild_only=True,
    default_member_permissions=Permissions(manage_channels=True),
)(commands.update_channel)
bot.slash_command(
    name="link",
    desciption="Register a new attendance code link",
)(commands.link)
bot.slash_command(
    name="dialog",
    desciption="Demo Dialog Box",
)(commands.dialog)


bot.run(bot_config.token)
