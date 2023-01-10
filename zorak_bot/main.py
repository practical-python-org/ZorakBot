import os
import sys
import toml
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '/', intents=discord.Intents.all())

channels = toml.load('test_server.toml')['channels']
logging = channels['log_channels']
user_roles = toml.load('test_server.toml')['user_roles']


def load_cogs():
        for f in os.listdir("./cogs"):
                if f.endswith(".py"):
                    bot.load_extension("cogs." + f[:-3])

def load_key_and_run():
    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
        bot.run(TOKEN)
    else:
        print('ERROR: You must include a bot token.')

if __name__ == "__main__":
    load_cogs()
    load_key_and_run()






