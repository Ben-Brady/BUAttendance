from modules import students, cispr, config, commands
from modules.discord import TaskCog
import logging
import discord
from discord import Permissions
from discord.ext import tasks


intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
bot_config = config.Config()


@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')


bot.slash_command(
    name="set_channel",
    description="",
    guild_only=True,
    default_member_permissions=Permissions(manage_channels=True),
)(commands.update_channel)
bot.slash_command(
    name="link",
    description="Submit an attendance code link",
)(commands.link)
bot.slash_command(
    name="manual_register",
    description="Manually register for automatic attendance",
)(commands.manual_register)
bot.slash_command(
    name="unregister",
    description="Unregister for automatic attendance",
)(commands.unregister)

bot.add_cog(TaskCog(bot))

bot.run(bot_config.token)
