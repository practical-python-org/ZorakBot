from discord.ext import commands
from ._settings import log_channel, admin_roles
from utilities.cog_helpers._embeds import embed_message_edit


class LoggingMessageEdit(commands.Cog):
    """
    Simple listener to on_message_edit
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        """
        Just checking if the content before is != to the content after.
        """
        if message_before.content != message_after.content:
            # This guy here makes sure we use the displayed name inside the guild.
            if message_before.author.nick is None:
                username = message_before.author
            else:
                username = message_before.author.nick

            author = message_before.author

            for role in message_before.author.roles:
                if role.id not in admin_roles.values():
                    """
                    Dont log admin actions.
                    This just gets really messy when we are cleaning things up
                    or doing dodgy business in secret places. 
                    """
                    embed = embed_message_edit(username, author, message_before, message_after)
                    logs_channel = await self.bot.fetch_channel(log_channel["chat_log"])
                    await logs_channel.send(embed=embed)
                    return


def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingMessageEdit(bot))
