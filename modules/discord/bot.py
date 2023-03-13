from . import TaskCog, commands
import discord
import logging

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')
    await task_cog.start()

commands.register_commands(bot)

task_cog = TaskCog(bot)
bot.add_cog(task_cog)


def start_bot(token: str):
    bot.run(token)
