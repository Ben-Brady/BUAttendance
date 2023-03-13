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
        try:
            new_token = cispr.refresh_token(token)
        except cispr.CisprSessionExpiredError:
            owner = self.bot.get_user(264536525054672906)
            if isinstance(owner, discord.User):
                await self.alert_bot_developer(owner)
        else:
            cispr.set_global_token(new_token)

    async def alert_bot_developer(self, owner: discord.User):
        await owner.send(
            embed=discord.Embed(
                title="WARNING: Your CISPR Session Expired",
                description="You must place a new session token in ./data/cispr_session"
            )
        )

    @tasks.loop(hours=1)
    async def task_refresh_user_tokens():
        for user in users.iter_users():
            new_token = cispr.refresh_token(user.session_token)
            users.update(
                discord_id=user.discord_id,
                session_token=new_token,
            )
