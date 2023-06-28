"""
Detects message links, and sends a preview of the message that is linked.
"""
import math
import discord
from discord.ext import commands


class UtilityPreview(commands.Cog):
    """Detects message links, and sends a preview of the message that is linked."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Detects message links, and sends a preview of the message that is linked.
        """
        text = message.content
        text = text.split(" ")
        for word in text:
            if word.startswith("https://discord.com/channels/") is True:

                link = word.split("/")
                sourceserver = self.bot.get_guild(int(link[4]))
                sourcechannel = sourceserver.get_channel(int(link[5]))
                sourcemessage = await sourcechannel.fetch_message(int(link[6]))

                if len(sourcemessage.content) <= 1000:
                    embed = discord.Embed(
                        title="Link preview: ",
                        description=f"Length: {len(sourcemessage.content)}",
                    )
                    embed.add_field(name="Content:", value=sourcemessage.content)
                    embed.set_footer(text=sourcemessage.author)
                    await message.channel.send(embed=embed)

                elif len(sourcemessage.content) > 1000:
                    contents = sourcemessage.content
                    con2 = []
                    splitstr = math.ceil(len(contents) / 1000)
                    embed1 = discord.Embed(
                        title="Link preview: ",
                        description=f"Length: {len(sourcemessage.content)}",
                    )
                    while contents:
                        con2.append(contents[:900])
                        contents = contents[900:]
                    for feilds in range(0, splitstr):
                        embed1.add_field(
                            name="------",
                            value=f"```py\n{con2[feilds]}\n```",
                            inline=False,
                        )
                    embed1.set_footer(text=sourcemessage.author)
                    await message.channel.send(embed=embed1)


def setup(bot):
    """Required."""
    bot.add_cog(UtilityPreview(bot))
