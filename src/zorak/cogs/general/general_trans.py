"""
A cog that adds translations to Zorak using the googletrans library
"""

import logging

import discord
from discord.ext import commands
from googletrans import Translator, LANGUAGES


logger = logging.getLogger(__name__)

with open("../../utilities/cog_helpers/whitelist.txt") as f:
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
        self.threshold = 0.70   #! Does this do anything?

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Scans every message for non-english content.
        """
        if message.author.bot:
            return

        if message.content.lower() in WHITE_LIST:
            return

        if len(message.content) < 7: #! we don't translate short words? like if someone types かわいい??
            return

        detected = self.translator.detect(message.content)
        multi_lang = is_multi_lang(detected.lang)

        if 'en' in detected.lang:
            """
            I worry how this works. If multiple languages are detected you would supposedly get a list
            like ["es", "en"], correct? But if multiple languages are not detected, you would get a 
            string like "en". Correct me if I'm wrong but it feels a bit like sloppy coding to check 
            if x is in [either a list or a string]... because outside of this case, the condition would
            be true if you either had a list that looked like ["ab", "cd", "en"] or if you had a 
            string like "armenian".  I know this wont happen because you would only get languages codes
            from detected.lang, but I would like to do things nicely. Perhaps move this condition to the
            following lines where we treat detected.lang differently depending on if it is multi_lang or not.
            """
            # If the message is english 70% english, just stop
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

        # send results of translation as embed
        embed = discord.Embed(
            title=f"{message.content}:",
            description=f"{translation.text}")

            footer = f"translated from {detected_language}\nconfidence: {confidence * 100:0.2f}%"
            pronunciation = translation.extra_data["translation"][1:]
            if pronunciation:
                footer += f"\npronunciation: ({pronunciation[0][-1].lower()})"

        embed.set_footer(text=footer)
        await message.channel.send(embed=embed)

    @commands.slash_command()
    async def translate(self, ctx, source_language, text):
        """
        A command to specify a translation.
        """
        logger.info("%s used the %s command.", ctx.author.name, ctx.command)
        try:
            translated = self.translator.translate(text, dest=source_language)
            embed = discord.Embed(
                title=f"{text}:",
                description=translated.text
            )
            footer = f"translated from {LANGUAGES[source_language]}"
            pronunciation = translation.extra_data["translation"][1:]
            if pronunciation:
                footer += f"\npronunciation: ({pronunciation[0][-1].lower()})"

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
            embed.set_footer(text="Please use the 2 digit code for your desired language.\n(Chinese codes are 5 digits)")
            await ctx.respond(embed=embed)


def setup(bot):
    """Docstrings4lyfe"""
    bot.add_cog(GoogleTranslate(bot))
