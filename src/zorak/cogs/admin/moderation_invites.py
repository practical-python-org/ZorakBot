"""
A listener that looks for discord invite looking things and destroys them.
"""
import re
from datetime import datetime

import discord
from discord.ext import commands


class ModerationInvites(commands.Cog):
    """
    Destroying spam with Regex.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Scans every message with the regex below.
        """
        if not message.author.bot:
            txt = message.content
            current_channel = message.channel
            author = message.author
            settings = self.bot.db_client.get_guild_settings(message.guild)

            def is_invite(arg_message):
                """
                - invitation types
                -> Official covers official invites "discord.gg/s7s8df9a"
                -> unofficial urls that start with d and end with letter numbers "dxxxx.gg/23bn2u2"
                """
                official = re.search(
                    "(?:https?://)?(?:www\.|ptb\.|canary\.)?(?:discord(?:app)?\.(?:(?:com|gg)"  # pylint: disable=W1401
                    "/invite/[a-z0-9-_]+)|discord\.gg/[a-z0-9-_]+)",  # pylint: disable=W1401
                    arg_message,
                )
                unofficial = re.search(
                    "(?:https?://)?(?:www\.)?(?:dsc\.gg|invite\.gg+|discord\.link)"  # pylint: disable=W1401
                    "/[a-z0-9-_]+",  # pylint: disable=W1401
                    arg_message,
                )
                if official is not None or unofficial is not None:
                    return True
                return False

            def log_message(arg_message):
                """
                If it finds something, it logs the message
                """
                author = arg_message.author
                embed = discord.Embed(
                    title="<:red_circle:1043616578744357085> Invite removed",
                    description=f"Posted by {arg_message.author}\nIn {'a DM.' if isinstance(arg_message.channel, discord.DMChannel) else arg_message.channel.mention}",
                    color=discord.Color.dark_red(),
                    timestamp=datetime.utcnow(),
                )
                embed.set_thumbnail(url=author.avatar)
                embed.add_field(
                    name="Message: ",
                    value=message.content,  # ToDo: This throws an error when deleting an embed.
                    inline=True,
                )
                return embed

            def embed_warning(arg_message):
                """
                If it finds something, it sends a warning that the user should quit that shit.
                """
                embed = discord.Embed(
                    title="<:x:1055080113336762408> External Invites are not allowed here!",
                    description=f"{arg_message.author}, your message was removed "
                                f"because it contained an external invite.\nIf this "
                                f"was a mistake, contact the @staff",
                    color=discord.Color.dark_red(),
                    timestamp=datetime.utcnow(),
                )
                return embed

            def check_for_admin_override(arg_message):
                """
                Handling for when a MOD user needs to post an invitation
                """
                if not message.content.startswith('z.invite '):
                    return False

                return any(role.id in settings.admin_roles.values() for role in message.author.roles)

            if is_invite(txt):
                if isinstance(message.channel, discord.DMChannel):
                    return

                if not check_for_admin_override(txt):
                    logs_channel = await self.bot.fetch_channel(settings["mod_log"])
                    await logs_channel.send(embed=log_message(message))
                    await message.delete()
                    await current_channel.send(embed=embed_warning(message))


def setup(bot):
    """
    Required.
    """
    bot.add_cog(ModerationInvites(bot))
