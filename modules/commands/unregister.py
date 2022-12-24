from modules import cispr, database
from discord.commands.context import ApplicationContext


async def unregister_command(ctx: ApplicationContext):
    await ctx.send("Unregister")

