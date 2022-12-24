from modules.discord import send_attendance_code, SendAttedanceCodeError
from modules.cispr._code import AttendanceCode, SessionCreationError
from discord.commands import ApplicationContext


async def link_command(ctx: ApplicationContext, link: str):
    # TODO: Check Exists
    try:
        session = AttendanceCode.from_link(link)
    except SessionCreationError:
        await ctx.respond("Could Not Parse Attendance Code", delete_after=5)
        return

    try:
        await send_attendance_code(ctx.bot, session)
    except SendAttedanceCodeError:
        await ctx.respond("Could Not Send Announcement Message", delete_after=5)
        return

    await ctx.respond("Successfully Announced New Attendance Code", delete_after=5)
