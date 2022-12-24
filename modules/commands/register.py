from modules import signup
import string
import discord
from discord.commands.context import ApplicationContext


class RegisterModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label="Seminar Group",
            style=discord.InputTextStyle.singleline,
            required=True,
            min_length=1,
            max_length=1,
            placeholder="F",
        ))

        self.add_item(discord.ui.InputText(
            label="University Email",
            style=discord.InputTextStyle.singleline,
            required=True,
            min_length=26,
            max_length=26,
            placeholder="s1234567@bournemouth.ac.uk",
        ))

        self.add_item(discord.ui.InputText(
            label="Session Token",
            style=discord.InputTextStyle.long,
            required=True,
            min_length=200,
            placeholder=(string.ascii_lowercase * 10)[:97] + "...",
        ))

    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id  # type: ignore
        seminar_group = self.children[0].value or ""
        seminar_group = seminar_group.upper()
        email = self.children[1].value or ""
        token = self.children[2].value or ""

        try:
            signup.signup_user(
                user_id=user_id,
                seminar_group=seminar_group.upper(),
                email=email,
                token=token,
            )
        except signup.SignupFailure as e:
            title = "Failed To Sign Up"
            description = f"{e}"
        else:
            title = f"Successfully Signed Up"
            description = f"User: <@{user_id}>"
        
        embed = discord.Embed(
            title=title,
            description=description,
            fields=[
                discord.EmbedField(name="Seminar Group", value=seminar_group),
                discord.EmbedField(name="Email", value=email),
                discord.EmbedField(name="Session Token", value=token[:20] + "..."),
            ],
        )
        await interaction.response.send_message(embeds=[embed])



async def register_command(ctx: ApplicationContext):
    modal = RegisterModal(title="Register Automatic Attendance")
    await ctx.send_modal(modal)
