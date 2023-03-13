from modules import cispr, attendance
from modules.config import Config
from modules.cispr import AttendanceCode
from discord import ApplicationContext, SlashCommand

async def _command(ctx: ApplicationContext, link: str):
    async def respond(message: str):
        await ctx.interaction.response.send_message(
            content=message,
            ephemeral=True
        )
    
    try:
        code = AttendanceCode.from_link(link)
        await attendance.add_new_code(code)
        await respond(":white_check_mark: Successfully announced the new code")
    except cispr.AttendanceLinkParsingError:
        await respond(":x: You provided an invalid link")
    except attendance.CodeAlreadyAnnounced:
        await respond(":x: That attendance code has already been announced")
    except attendance.CouldNotSendAnnouncmenetMessage:
        await respond(f":x: Unable to send announcement message in <#{Config.attendence_channel}>")
    except cispr.CisprSessionExpiredError:
        await respond(":x: The bot's CISPR session has expired")
        raise


link_command = SlashCommand(
    func=_command,
    name="link",
    description="Submit an attendance code link",
)
