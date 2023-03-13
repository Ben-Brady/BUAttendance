from modules.config import _Config
from discord import SlashCommand, ApplicationContext, Permissions


config = _Config()

async def _command(ctx: ApplicationContext):
    config.attendence_channel = ctx.channel.id
    await ctx.interaction.response.send_message(
        content="Successfully changed attendance channel to here",
        ephemeral=True,
    )


update_channel_command = SlashCommand(
    func=_command,
    name="set_channel",
    description="Set the announcement channel",
    guild_only=True,
    default_member_permissions=Permissions(manage_channels=True),
)
