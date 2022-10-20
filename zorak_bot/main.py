import os
import sys
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

bot = commands.Bot()

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






