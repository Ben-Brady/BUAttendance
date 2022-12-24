from modules import qrcode
from modules.discord import download_image, Response
import discord
from discord.commands.context import ApplicationContext


async def dialog_command(ctx: ApplicationContext):
    modal = RegisterModal(title="Register Automatica Attendance")
    await ctx.send_modal(modal)


class RegisterModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label="University Email",
            style=discord.InputTextStyle.singleline,
            max_length=100,
            required=True,
            placeholder="1234567@bournemouth.ac.uk",
        ))
        self.add_item(discord.ui.InputText(
            label="Session Token",
            style=discord.InputTextStyle.long,
            required=True,
            placeholder="abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzab",
        ))

    async def callback(self, interaction: discord.Interaction):
        name = interaction.user.display_name # type:    ignore
        embed = discord.Embed(title=f"{name.title()} Attendance Successfully Registered")
        await interaction.response.send_message(embeds=[embed])
