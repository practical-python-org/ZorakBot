import logging
import os

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from zorak_bot.api import create_app
from zorak_bot.util import clean_path
from zorak_bot.util.args_util import parse_args
from zorak_bot.util.logging_util import setup_logger

logger = logging.getLogger(__name__)

bot = Bot(command_prefix=["z.", "Z."])
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you..."))
    print("{0.user}, ready to conquer the world.".format(bot))


@bot.listen("on_message")  # What this do?
async def preview(message):
    if (
        message.content.startswith("https://discord.com/channels/") is True
        or message.content.startswith("https://discordapp.com/channels/") is True
    ):
        try:
            link = message.content.replace("/", " ").split(" ")
            source_channel = bot.get_guild(int(link[4])).get_channel(int(link[5]))
            source_message = await source_channel.fetch_message(int(link[6]))
            embed = discord.Embed(title="**Message** **Preview**", description="", timestamp=source_message.created_at)
            if len(source_message.content) <= 1000:
                embed.add_field(name="**Content:** ", value=source_message.content)
            elif len(source_message.content) > 1000:
                # This just breaks the source message into 950 character chunks in a list.
                chunks = [source_message.content[i : i + 950] for i in range(0, len(source_message.content), 950)]
                for chunk in chunks:  # for each item in the chunk list, add a field to the embed.
                    embed.add_field(name="**---------**", value=f"```py\n{chunk}\n```", inline=False)
            embed.set_footer(text=source_message.author, icon_url=source_message.author.avatar_url)
            await message.channel.send(embed=embed)
        except:
            await message.channel.send(
                f"         -**Cannot** **preview**-\n-" f"**Make sure message is in this server," f" and not a text file or image**-"
            )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("User you requested cannot be found.", reference=ctx.message)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Zorak has no such command!", reference=ctx.message)
    await ctx.message.delete()


def load_cog(cog_name):
    try:
        bot.load_extension(cog_name)
        logger.info(f"Loaded Extension {cog_name}")
    except Exception as e:
        exc = f"{type(e).__name__}: {e}"
        logger.info(f"Failed to load extension {cog_name}: {exc}")


def load_core_cogs():
    """
    Simple sutoloader for our main cogs, all cogs under core/cogs/auto_load get loaded automatically on startup,
    and we manually load the optional ones. Or can even load them via commands (only owner/admin functionalities.)
    """
    logger.info("Attempting to load Cogs")
    path = clean_path("./zorak_bot/core/cogs/auto_load")
    for file in os.listdir(path):
        if file.endswith(".py"):
            load_cog(f"core.cogs.auto_load.{file[:-3]}")


def main() -> None:
    args = parse_args()
    setup_logger(level=args.log_level, stream_logs=args.console_log, log_file=args.log_file, err_file=args.err_file)
    logger.info(f"Arguments Passed {args}")
    logger.info("Logger initialised")

    auto_persist = True
    if args.flask_host and args.flask_port:
        logger.info("Attempting to launch background Flask API.")
        try:
            app = create_app(seperate_thread=True)
            app.run(host=args.flask_host, port=args.flask_port)
            auto_persist = False
            logger.info("Successful in launching background Flask API.")
        except Exception as e:
            logger.error(f"Failed launch of background Flask API with error: {str(e)}")
    if auto_persist:
        logger.info("No Flask API config detectd - running in auto-persist mode.")
        load_cog("core.cogs.optional.auto_persist")

    load_core_cogs()
    logger.info("Attempting to run Zorak")
    if args.discord_token is not None:
        bot.run(args.discord_token)
    else:
        bot.run(os.environ["TOKEN"])


if __name__ == "__main__":
    main()
