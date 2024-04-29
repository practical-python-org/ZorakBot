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
    return [string[i : i + chunk_size] for i in range(0, len(string), chunk_size)]


class UtilityRunCode(commands.Cog):
    """Uses PistonAPI to run code in the server."""

    def __init__(self, bot):
        self.bot = bot

    def get_embed(self, name, value, channel, is_error=False):
        if is_error:
            embed = discord.Embed(colour=discord.Colour.red(), title="Oops...")
        else:
            embed = discord.Embed(colour=discord.Colour.green(), title="Python 3.10")

        size = 11  # start counting how big the embed is.
        max_size = 1000  # Default to 1000 chars.

        # Check if the user is in the bot_spam channel, to allow for larger embeds.
        print(self.bot.server_settings.normal_channel)
        if channel.id == self.bot.server_settings.normal_channel["bot_spam_channel"]:
            max_size = 6000  # Discord limitation

        # Discord only supports fields with 1024 chars
        for i, field in enumerate(chop_dat_boi_up(value, 500)):
            size += len(field)
            # Discord only supports EMBEDS with a total character size of 6000
            if size < max_size:
                print(field)
                embed.add_field(
                    name=name if i == 0 else "\u200b", value=field, inline=i != 0
                )
            # pylint: disable=W1401
        return embed

    @commands.command()
    async def run(self, ctx, *, codeblock):
        """
        Uses Piston-API to run code in the server.
        """
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)

        # Adjust iOS quotation marks “”‘’ to avoid SyntaxError: invalid character
        for i, c in enumerate("“‘”’"):
            codeblock = codeblock.replace(c, "\"'"[i % 2])

        if codeblock.startswith("```py") and "```" in codeblock[3:]:
            # Split input args from codeblock
            _, codeblock, args = codeblock.split("```")
            args = args.strip()

            # Remove py/python language indicator from codeblock
            codeblock = codeblock.removeprefix("py").removeprefix("thon").strip()

            # Check for input() args and calls to input() function
            if "input(" in codeblock and not args:
                value = (
                    "I am happy to run your script but I do not want to interact with you. You can "
                    "remove your input() functions, however if you insist on keeping them, please "
                    "put your input values in order on separate lines after the codeblock:\n\n"
                    '\`\`\`py \nx = input("What is your first input: ")\ny = input("What is '
                    'your second input: ")\nprint(x)\nprint(y)\n\`\`\`\nmy_first_input\nmy_second_input'
                )

            else:
                # Try executing the code
                piston = PistonAPI()
                runcode = piston.execute(
                    language="py", version="3.10.0", code=codeblock, stdin=args
                )

                # Check for EOFError
                if all(item in runcode for item in ("Traceback", "EOFError:")):
                    value = (
                        "The function input() was called more times than the number of inputs provided.\n"
                        "Make sure you have the correct number of input strings after the codeblock.\n"
                        "(Each input string should be separated by a new line)\n\n"
                        '\`\`\`py \nx = input("What is your first input: ")\ny = input("What is '
                        'your second input: ")\nprint(x)\nprint(y)\n\`\`\`\nmy_first_input\nmy_second_input'
                    )

                # Code execution successful without EOFError
                else:
                    embed = self.get_embed("Output:", runcode, ctx.channel)
                    message = await ctx.reply(embed=embed)
                    return

        # Check for single quotes instead of codeblocks
        elif codeblock.startswith("'''") or codeblock.endswith("'''"):
            value = (
                "Did you mean to use a \` instead of a ' ?\n\n"
                "\`\`\`py \nx = 'like this'\nprint(x) \n\`\`\`"
            )
        else:
            value = (
                "Please place your code inside a code block. (between \`\`\`py "
                "and \`\`\`)\n\n\`\`\`py \nx = 'like this'\nprint(x) \n\`\`\`"
            )

        # Output error message
        embed = self.get_embed("Formatting error", value, ctx.channel, True)
        message = await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            # Ignore messages sent by bots
            return
        if before.content.startswith("/run") or after.content.startswith("/run"):
            # Make sure we ONLY re-run messages that are /run commands
            channel = after.channel  # The channel that the edited message is in
            # Grab the last 10 (should be enough...) bot messages
            all_replies = [
                message
                async for message in channel.history(limit=20)
                if message.author == self.bot.user
            ]
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
