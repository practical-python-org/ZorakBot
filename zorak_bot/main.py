import os
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

bot = commands.Bot()

if __name__ == "__main__":
    for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                bot.load_extension("cogs." + f[:-3])

    bot.run("TOKEN")


