"""
Listener to scan for exe or zip files.
"""
import logging

from discord.ext import commands

from zorak.utilities.cog_helpers._embeds import embed_cant_do_that

logger = logging.getLogger(__name__)


class FiletypeChecker(commands.Cog):
    """
    Listener to check if a exe file or a zip file is attached in
    a user's message to prevent malicious files from being sent.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        for attachment in message.attachments:
            print(f"content type: {attachment.content_type}")
            if attachment.content_type in [
                "application/x-msdownload",
                "application/x-dosexec",
                "application/x-msdos-program",
                "application/octet-stream",
                "application/x-binary",
                "application/x-mach-binary",
                "application/x-apple-diskimage",
                "application/java-archive",
                "application/x-java-class",
                "application/zip",
                "application/x-zip-compressed",
                "multipart/x-zip",
                "application/x-compressed",
                "application/x-compress",
                "application/x-zip",
                "application/zip-compressed",
                "multipart/x-compressed",
            ]:
                await message.delete()
                await message.channel.send(
                    embed=embed_cant_do_that(
                        "You cannot send executable files or zip files."
                    ),
                    delete_after=10,
                )
                logger.info(
                    f"Blocked attachment from {message.author}:\n{message.clean_content}\nAttachment:{attachment.filename}"
                )
                return


def setup(bot):
    """
    required.
    """
    bot.add_cog(FiletypeChecker(bot))
