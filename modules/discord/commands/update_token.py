from modules import cispr
from discord import SlashCommand, ApplicationContext, Permissions

async def _command(ctx: ApplicationContext, token: str):
    if not cispr.check_token(token):
        await ctx.interaction.response.send_message(
            content="Failed, Invalid Token Provided",
            ephemeral=True,
        )
    else:
        cispr.set_global_token(token)
        await ctx.interaction.response.send_message(
            content="Success, Updated Global Token",
            ephemeral=True,
        )

update_token_command = SlashCommand(
    func=_command,
    name="update_token",
    description="Update the current CISPR token",
    default_member_permissions=Permissions(administrator=True),
)