from modules import cispr
from modules.database import users

import discord
from discord.ext import tasks


class TaskCog(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot


    async def start(self):
        await self.task_refresh_global_token.start()
        await self.task_refresh_user_tokens.start()


    @tasks.loop(hours=1)
    async def task_refresh_global_token(self):
        token = cispr.get_global_token()
        owner = self.bot.get_user(264536525054672906)
        try:
            new_token = cispr.refresh_token(token)
        except cispr.CisprSessionExpiredError:
            if isinstance(owner, discord.User):
                await owner.send(
                    "WARNING: Your cispr_session has expired \n" \
                    "You need to update it or chaos will ensue"
                )
        else:
            cispr.set_global_token(new_token)


    @tasks.loop(hours=1)
    async def task_refresh_user_tokens():
        for user in users.iter_users():
            new_token = cispr.refresh_token(user.session_token)
            users.update(
                discord_id=user.discord_id,
                session_token=new_token,
            )
