from modules import cispr, attendance
from discord import ApplicationContext, SlashCommand


async def _command(ctx: ApplicationContext, progress_code: str):
    try:
        code = cispr.AttendanceCode.from_code(
            progress_code,
            academic_year="22/23",
            level="Level 4"
        )
        await attendance.add_new_code(code)
    except cispr.AttendanceCodeParsingError:
        await ctx.interaction.response.send_message(
            content="You have provided an invalid link",
            ephemeral=True
        )
        return
    except cispr.CisprSessionExpiredError:
        await ctx.interaction.response.send_message(
            content="The bot's CISPRS session has expired",
            ephemeral=True
        )
        raise
    except attendance.CodeAnnouncementFailure as e:
        await ctx.interaction.response.send_message(
            content=str(e),
            ephemeral=True,
        )
        raise
    
    await ctx.interaction.response.send_message(
        "Successfully Announced New Code",
        ephemeral=True,
    )


code_command = SlashCommand(
    func=_command,
    name="code",
    description="Submit an attendance progress code",
)
