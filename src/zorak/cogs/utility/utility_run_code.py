"""
Uses PistonAPI to run code in the server.
"""
import logging
import re

from pistonapi import PistonAPI
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


def chop_dat_boi_up(string, chunk_size):
    # vOmIt #
    return [string[i:i + chunk_size] for i in range(0, len(string), chunk_size)]


class UtilityRunCode(commands.Cog):
    """Uses PistonAPI to run code in the server."""

    def __init__(self, bot):
        self.bot = bot

    def get_embed(self, name, value, is_error=False):
        if is_error:
            embed = discord.Embed(colour=discord.Colour.red(), title="Oops...")
        else:
            embed = discord.Embed(colour=discord.Colour.green(), title="Python 3.10")

        for i, field in enumerate(chop_dat_boi_up(value, 1000)):  # Discord only supports fields with 1024 chars
            if i != 0:
                if i <= 25:  # Discord only supports 25 add_fields
                    embed.add_field(
                        name="\u200b",
                        value=field,
                        # pylint: disable=W1401
                    )
            else:
                embed.add_field(
                    name=name,
                    value=field,
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

        # Adjust iOS quotation marks “”‘’ to avoid SyntaxError: invalid character
        for i, c in enumerate("“‘”’"):
            codeblock = codeblock.replace(c, "\"'"[i % 2])

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
                    value = 'I am happy to run your script but I do not want to interact with you. You can ' \
                            'remove your input() functions, however if you insist on keeping them, please ' \
                            'put your input values in order on separate lines after the codeblock:' \
                            '\n\n\`\`\`py \nx = input("What is your first input: ")\ny = input("What is ' \
                            'your second input: ")\nprint(x)\nprint(y)\n\`\`\`\nmy_first_input\nmy_second_input'
                    embed = self.get_embed("Formatting error", value, True)
                    message = await ctx.channel.send(embed=embed)
                    # self.previous_message_id = message.id
                    return
                # Else, replace all input()s with values
                else:
                    for i in re.findall(r"input\(.*\)\n", codeblock):
                        codeblock = codeblock.replace(i, f'"""{args.pop(0)}"""\n', 1)

            piston = PistonAPI()
            runcode = piston.execute(language="py", version="3.10.0", code=codeblock)
            embed = self.get_embed("Output:", runcode)
            message = await ctx.reply(embed=embed)

        elif codeblock.startswith("'''") and codeblock.endswith("'''"):
            value = "Did you mean to use a \` instead of a ' ?\n\`\`\`py Your code here \`\`\`"
            embed = self.get_embed("Formatting error", value, True)
            message = await ctx.channel.send(embed=embed)

        else:
            print(codeblock)
            value = 'Please place your code inside a code block. (between \`\`\`py ' \
                    'and \`\`\`)\n\n\`\`\`py \nx = "like this"\nprint(x) \n\`\`\`'
            embed = self.get_embed("Formatting error", value, True)
            message = await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            # Ignore messages sent by bots
            return
        if before.content.startswith('/run') or after.content.startswith('/run'):
            # Make sure we ONLY re-run messages that are /run commands
            channel = after.channel  # The channel that the edited message is in
            # Grab the last 10 (should be enough...) bot messages
            all_replies = [message async for message in channel.history(limit=20) if message.author == self.bot.user]
            for bot_reply in all_replies:
                if bot_reply.reference.message_id == after.id:
                    await bot_reply.delete()
                    # If the reference message of the bot message is the edited message...
                    # Re-run the /run command with the new content
                    # however, we dont call the command with /run, so we need to remove the '/run' from the message
                    code = after.content.replace("/run", "").strip()
                    new_ctx = await self.bot.get_context(after)  # get a new message ctx
                    return await new_ctx.command.callback(self, new_ctx, codeblock=code)


def setup(bot):
    """Required."""
    bot.add_cog(UtilityRunCode(bot))
