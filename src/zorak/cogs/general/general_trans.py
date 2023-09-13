"""
A cog that adds translations to Zorak using the googletrans library
"""

import logging

import discord
from discord.ext import commands
from googletrans import Translator, LANGUAGES
from pathlib import Path

logger = logging.getLogger(__name__)


with open(Path.cwd().joinpath("src", "zorak", "utilities", "cog_helpers", "whitelist.txt")) as f:
    WHITE_LIST = f.read().splitlines()


def is_multi_lang(lang):
    """Tests if input is a list."""
    return isinstance(lang, list)


class GoogleTranslate(commands.Cog):
    """Main class for googletrans"""

    def __init__(self, bot):
        """
        Here we innit the bot, the translator object,
        and our acceptable threshold
        """
        self.bot = bot
        self.translator = Translator()
        self.threshold = 0.75

    @staticmethod
    def pronunciation(message):
        """
        Static Method. Call with GoogleTranslate.pronunciation(message)
        Looks up the pronunciation from the extra data
        """
        if message:
            message = [*filter(None, message[0])]
            return f"\npronunciation: ({message[0].lower()})"
        return ""

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Scans every message for non-english content.
        """
        if message.author.bot:
            return

        if message.content.lower() in WHITE_LIST:
            return

        detected = self.translator.detect(message.content)
        multi_lang = is_multi_lang(detected.lang)

        if 'en' in detected.lang:
            """
            # If the message is english just stop, do nothing.
            """
            return

        if 'en' not in detected.lang and detected.confidence < self.threshold:
            """
            If the language is not detected as english, 
            and the CONFIDENCE that it is something else is low... dont do anything.
            """
            return

        logger.info("A message by %s was translated.", message.author.name)
        if multi_lang:
            lang = detected.lang[0].lower()
            lang_2 = detected.lang[1].lower()
            confidence = detected.confidence[0]  # extract value from confidence list
            detected_language = f"{LANGUAGES[lang]}, {LANGUAGES[lang_2]}".title()

        else:
            lang = detected.lang.lower()
            confidence = detected.confidence
            detected_language = LANGUAGES[lang].title()

        # translate message
        translation = self.translator.translate(message.content, dest='en')

        if translation.text.strip().lower() == message.content.strip().lower():
            """
            Check to see if the result is the same as the original. If so, do not print
            This is to avoid spamming random haha's and hehehe's. (Thanks Crambor!)
            """
            return

        # send results of translation as embed
        embed = discord.Embed(
            title=f"{message.content}:",
            description=f"{translation.text}")

        footer = f"translated from {detected_language}\nconfidence: {confidence * 100:0.2f}%"
        footer += GoogleTranslate.pronunciation(translation.extra_data["translation"][1:2])

        embed.set_footer(text=footer)
        await message.channel.send(embed=embed)

    @commands.slash_command()
    async def translate(self, ctx, destination_language, text):
        """
        A command to specify a translation.
        """
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)
        try:
            translation = self.translator.translate(text, dest=destination_language)
            embed = discord.Embed(
                title=f"{text}:",
                description=translation.text
            )
            footer = f"translated from {LANGUAGES[translation.src]}"
            footer += GoogleTranslate.pronunciation(translation.extra_data["translation"][1:2])

            embed.set_footer(text=footer)
            await ctx.respond(embed=embed)

        except ValueError as v:
            count = 0
            languages = ""
            n = 3
            # Print languages & codes n (3) to a row
            for key, value in LANGUAGES.items():
                if count % n == 0:
                    languages += "\n"
                languages += f"{value.title()}-{key}".ljust(30)
                count += 1

            embed = discord.Embed(
                title="Valid Language Codes:",
                description=languages
            )
            embed.set_footer(
                text="Please use the 2 digit code for your desired language.\n(Chinese codes are 5 digits)")
            await ctx.respond(embed=embed)


def setup(bot):
    """Docstrings4lyfe"""
    bot.add_cog(GoogleTranslate(bot))
