from pickledb import PickleDB
import os


class InvalidConfigException(Exception):
    pass


class Config:
    def __init__(self):
        self.db = PickleDB("./config.json", True, True)
        if not self.db.exists("token"):
            self.db.set("token", "")
    
    
    def _get_token(self) -> str:
        token = os.getenv("BOT_TOKEN") or self.db.get("token")
        
        if not isinstance(token, str) or token == "":
            raise InvalidConfigException(
                "No discord bot token specified, "
                "Either set the enviroment variable BOT_TOKEN "
                "or add 'token' to config.json"
            )

        return token

    def _get_attendence_channel(self) -> int | None:
        channel = self.db.get("attendance_channel")
        if isinstance(channel, int):
            return channel
        else:
            return None


    def _set_attendence_channel(self, value: int):
        self.db.set("attendance_channel", value)

    
    token = property(_get_token)
    attendence_channel = property(_get_attendence_channel, _set_attendence_channel)
