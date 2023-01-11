import os
import sys
import toml
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '/', intents=discord.Intents.all())

channels = toml.load('server.toml')['channels']
mod_channels = channels['moderation']
log_channels = channels['log_channels']
normal_channels = channels['normal_channels']

user_roles = toml.load('server.toml')['user_roles']
admin_roles = user_roles['admin']
elevated_roles = user_roles['elevated']
badboi_role = user_roles['bad']
unverified_role = user_roles['unverified']


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






