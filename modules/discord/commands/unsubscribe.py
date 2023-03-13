# from . import SlashCommand
from modules import cispr, database
from discord import ApplicationContext, Bot, SlashCommand


async def _command(ctx: ApplicationContext):
    if database.users.exists(ctx.user.id):
        await ctx.interaction.response.send_message(
            content="You are not subscribed",
            ephemeral=True,
        )
        return
    else:
        database.users.delete(ctx.user.id)
        await ctx.interaction.response.send_message(
            content="Successfully unsubscribed from automatic attendance",
            ephemeral=True,
        )

unsubscribe_command = SlashCommand(
    func=_command,
    name="unsubscribe",
    description="Unsubscribe for automatic attendance",
)
