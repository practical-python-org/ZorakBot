#import discord
from discord.ext import commands


def get_error_msg(error):
    if isinstance(error, commands.MemberNotFound):
        return "User you requested cannot be found."
    elif isinstance(error, commands.CommandNotFound):
        return "Zorak has no such command!"
    elif isinstance(error, commands.MissingPermissions):
        return "You do not have permission to use this command."