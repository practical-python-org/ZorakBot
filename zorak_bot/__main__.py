import logging
import os
import sys

import discord
from discord.ext import commands
from utilities.core.args_utils import parse_args
from utilities.core.logging_utils import setup_logger

logger = logging.getLogger("discord")
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
bot.remove_command("python")


def load_cogs():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            if not "_init_" in f:
                bot.load_extension("cogs." + f[:-3])


def load_key_and_run():
    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
        bot.run(TOKEN)
    else:
        print("ERROR: You must include a bot token.")


if __name__ == "__main__":
    args = parse_args()
    setup_logger(level=args.log_level, stream_logs=args.console_log)
    load_cogs()
    if args.discord_token is not None:
        bot.run(args.discord_token)
    else:
        load_key_and_run()
