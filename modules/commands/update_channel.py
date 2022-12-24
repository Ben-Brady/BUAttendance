from modules.config import Config
from discord.ext.commands import Context


config = Config()


async def update_channel_command(ctx: Context):
    config.attendence_channel = ctx.channel.id
    await ctx.reply("Successfully changed attendance channel to here")
