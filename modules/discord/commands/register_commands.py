from . import (
    link_command,
    code_command,
    update_token_command,
    update_channel_command
)
from discord import Bot


def register_commands(bot: Bot):
    bot.add_application_command(link_command)
    bot.add_application_command(code_command)
    bot.add_application_command(update_token_command)
    bot.add_application_command(update_channel_command)
    # bot.add_application_command(subscribe_command)
    # bot.add_application_command(unsubscribe_command)
