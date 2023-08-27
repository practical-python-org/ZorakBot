"""
A listener that looks for repeat messages and destroys them.
"""
from datetime import datetime, timedelta

from discord.ext import commands


class ModerationSpamMessages(commands.Cog):
    """
    Destroying spam with bots
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message_in_question):
        """
        Scans every message and compares them
        """
        time_ago = datetime.utcnow() - timedelta(minutes=5)

        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                async for last_message in channel.history(limit=10, after=time_ago):
                    if last_message.content == message_in_question.content:
                        if last_message.author == message_in_question.author and message_in_question.author.bot is False:
                            await last_message.channel.send(f"you already posted this in {message_in_question.channel.mention}")
                            await last_message.delete()

    # def log_message(arg_message):
    #     """
    #     If it finds something, it logs the message
    #     """
    #     author = arg_message.author
    #     embed = discord.Embed(
    #         title="<:red_circle:1043616578744357085> Invite removed",
    #         description=f"Posted by {arg_message.author}\nIn {arg_message.channel.mention}",
    #         color=discord.Color.dark_red(),
    #         timestamp=datetime.utcnow(),
    #     )
    #     embed.set_thumbnail(url=author.avatar)
    #     embed.add_field(
    #         name="Message: ",
    #         value=message.content,  # ToDo: This throws an error when deleting an embed.
    #         inline=True,
    #     )
    #     return embed

    # def embed_warning(arg_message):
    #     """
    #     If it finds something, it sends a warning that the user should quit that shit.
    #     """
    #     embed = discord.Embed(
    #         title="<:x:1055080113336762408> External Invites are not allowed here!",
    #         description=f"{arg_message.author}, your message was removed "
    #                     f"because it contained an external invite.\nIf this "
    #                     f"was a mistake, contact the @staff",
    #         color=discord.Color.dark_red(),
    #         timestamp=datetime.utcnow(),
    #     )
    #     return embed

    # if is_invite(txt) is True:
    #     logs_channel = await self.bot.fetch_channel(log_channel["mod_log"])
    #     await logs_channel.send(embed=log_message(message))
    #     await message.delete()
    #     await current_channel.send(embed=embed_warning(message))


def setup(bot):
    """
    Required.
    """
    bot.add_cog(ModerationSpamMessages(bot))
