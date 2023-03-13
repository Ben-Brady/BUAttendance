import discord
from discord.ext.commands import Context


class GuideView(discord.ui.View):
    ...


async def guide_command(ctx: Context):
    await ctx.reply("To Be Written")
