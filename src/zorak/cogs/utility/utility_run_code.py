"""
Uses PistonAPI to run code in the server.
"""
import logging
from pistonapi import PistonAPI
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class UtilityRunCode(commands.Cog):
    """Uses PistonAPI to run code in the server."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def run(self, ctx, *, codeblock):
        """
        Uses Piston-API to run code in the server.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)

        # Adjust iOS quotation marks “”‘’ to avoid SyntaxError: invalid character 
        codeblock.translate(codeblock.maketrans("“”‘’", """""''"""))

        piston = PistonAPI()
        if codeblock.startswith("```py") is True:
            if codeblock.endswith("```") is True:
                # Remove backticks and py/python language indicator from codeblock
                codeblock = codeblock.replace("```python", "").replace("```py", "").replace("```", "").strip()
            runcode = piston.execute(language="py", version="3.10.0", code=codeblock)
            embed = discord.Embed(colour=discord.Colour.green(), title="Python 3.10")
            embed.add_field(name="Output:", value=runcode)
            await ctx.channel.send(embed=embed)

        elif codeblock.startswith("'''") is True:
            if codeblock.endswith("'''") is True:
                embed = discord.Embed(colour=discord.Colour.red(), title="Oops...")
                embed.add_field(
                    name="Formatting error",
                    value="Did you mean to use a ` instead of "
                          "a '?\n\`\`\`py Your code here \`\`\`",  # pylint: disable=W1401
                )
                await ctx.channel.send(embed=embed)

        else:
            embed = discord.Embed(colour=discord.Colour.red(), title="Oops...")
            embed.add_field(
                name="Formatting error",
                value='Please place your code in a code block.'
                      '\n\nz.python \n\`\`\`py \nx = "like this"\nprint(x) \n\`\`\`'  # pylint: disable=W1401
            )
            await ctx.channel.send(embed=embed)


def setup(bot):
    """Required."""
    bot.add_cog(UtilityRunCode(bot))
