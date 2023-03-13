from modules import cispr, discord, database
import logging

class CodeAnnouncementFailure(Exception): pass
class CodeAlreadyAnnounced(CodeAnnouncementFailure): pass
class CouldNotSendAnnouncmenetMessage(CodeAnnouncementFailure): pass


async def add_new_code(code: cispr.AttendanceCode):
    if database.codes.exists(code.progress_code):
        raise CodeAlreadyAnnounced("Attendance Code Already Exists")
    
    try:
        await discord.send_attendance_code(code)
    except discord.SendAttedanceCodeError:
        raise CodeAnnouncementFailure("Could Not Send Announcement Message")

    # for user in database.users.iter_users():
    #     try:
    #         cispr.register_attendance(code, user.email)
    #     except Exception:
    #         logging.warning(f"Failed to register attendance for s{user.student_id}")

    database.codes.insert(code)
