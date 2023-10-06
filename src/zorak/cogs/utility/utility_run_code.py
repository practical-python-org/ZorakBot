"""
Uses PistonAPI to run code in the server.
"""
import logging
import re

from pistonapi import PistonAPI
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class UtilityRunCode(commands.Cog):
    """Uses PistonAPI to run code in the server."""

    def __init__(self, bot):
        self.bot = bot

    def get_embed(self, name, value, is_error=False):
        if is_error:
            embed = discord.Embed(colour=discord.Colour.red(), title="Oops...")
        else:
            embed = discord.Embed(colour=discord.Colour.green(), title="Python 3.10")
        embed.add_field(
            name=name,
            value=value,
            # pylint: disable=W1401
        )
        return embed

    @commands.command()
    async def run(self, ctx, *, codeblock):
        """
        Uses Piston-API to run code in the server.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        cleaner = self.bot.get_cog("MessageTrackerCleanup")

        # Deletes the previous embed if the original message has been edited
        if ctx.message.edited_at:
            try:
                previous_embed = await ctx.channel.fetch_message(cleaner.message_tracker[ctx.message.id]["embed_id"])
                if previous_embed:
                    await previous_embed.delete()
            except discord.NotFound:
                pass

        # Adjust iOS quotation marks “”‘’ to avoid SyntaxError: invalid character 
        for i, c in enumerate("“‘”’"):
            codeblock = codeblock.replace(c, "\"'"[i%2])

        if codeblock.startswith("```py") and "```" in codeblock[3:]:
            # Split input args from codeblock
            _, codeblock, args = codeblock.split("```")
            args = [arg for arg in args.split("\n") if arg]

            # Remove py/python language indicator from codeblock
            codeblock = codeblock.removeprefix("py").removeprefix("thon").strip()

            # Check for input() args or calls to input() function
            input_count = codeblock.count("input(")
            if args or input_count:
                # Check if number of input() functions matches args from user.
                if len(args) != input_count:
                    value = 'I am happy to run your script but I do not want to interact with you. You can'\
                            'remove your input() functions, however if you insist on keeping them, please '\
                            'put your input values in order on separate lines after the codeblock:'\
                            '\n\n\`\`\`py \nx = input("What is your first input: ")\ny = input("What is '\
                            'your second input: ")\nprint(x)\nprint(y)\n\`\`\`\nmy_first_input\nmy_second_input'
                    embed = self.get_embed("Formatting error", value, True)
                    message = await ctx.reply(embed=embed, mention_author=False)
                    cleaner.message_tracker[ctx.message.id] = {"created_at": ctx.message.created_at, "embed_id": message.id}
                    return
                # Else, replace all input()s with values
                else:
                    for i in re.findall(r"input\(.*\)\n", codeblock):
                        codeblock = codeblock.replace(i, f'"""{args.pop(0)}"""\n', 1)

            piston = PistonAPI()
            runcode = piston.execute(language="py", version="3.10.0", code=codeblock)
            embed = self.get_embed("Output:", runcode)
            message = await ctx.reply(embed=embed, mention_author=False)
            cleaner.message_tracker[ctx.message.id] = {"created_at": ctx.message.created_at, "embed_id": message.id}
            
        elif codeblock.startswith("'''") and codeblock.endswith("'''"):
            value = "Did you mean to use a \` instead of a ' ?\n\`\`\`py Your code here \`\`\`"
            embed = self.get_embed("Formatting error", value, True)
            message = await ctx.reply(embed=embed, mention_author=False)
            cleaner.message_tracker[ctx.message.id] = {"created_at": ctx.message.created_at, "embed_id": message.id}

        else:
            value = 'Please place your code inside a code block. (between \`\`\`py '\
                    'and \`\`\`)\n\n\`\`\`py \nx = "like this"\nprint(x) \n\`\`\`'
            embed = self.get_embed("Formatting error", value, True)
            message = await ctx.reply(embed=embed, mention_author=False)
            cleaner.message_tracker[ctx.message.id] = {"created_at": ctx.message.created_at, "embed_id": message.id}


def setup(bot):
    """Required."""
    bot.add_cog(UtilityRunCode(bot))
