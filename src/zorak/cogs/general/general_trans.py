"""
A cog that adds translations to Zorak using the googletrans library
"""

import logging

import discord.ext
import googletrans
from discord.ext import commands
from googletrans import Translator


logger = logging.getLogger(__name__)

whitelist = [
    "Python",
    "Variable",
    "Function",
    "Module",
    "List",
    "Tuple",
    "Dictionary",
    "Loop",
    "Conditional",
    "Class",
    "Inheritance",
    "Polymorphism",
    "Exception",
    "Object",
    "Method",
    "Argument",
    "Parameter",
    "Package",
    "Library",
    "Syntax",
    "Statement",
    "Import",
    "Return",
    "True",
    "False",
    "None",
    "Print",
    "Input",
    "File",
    "Error",
    "Debug",
    "IDE (Integrated Development Environment)",
    "Git",
    "GitHub",
    "Data",
    "Algorithm",
    "Algorithmic",
    "List Comprehension",
    "Dictionary Comprehension",
    "Recursion",
    "Lambda",
    "Generator",
    "Virtual Environment",
    "PIP (Python Package Index)",
    "Interpreter",
    "Bytecode",
    "GIL (Global Interpreter Lock)",
    "IDE (Interactive Development Environment)",
    "JSON (JavaScript Object Notation)",
    "API (Application Programming Interface)",
    "NumPy",
    "Pandas",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "TensorFlow",
    "Keras",
    "PyTorch",
    "Django",
    "Flask",
    "Requests",
    "Beautiful Soup",
    "SQLAlchemy",
    "NLTK",
    "OpenCV",
    "Pillow",
    "Gensim",
    "SciPy",
    "SymPy",
    "pytest",
    "unittest",
    "pytest-django",
    "pytest-cov",
    "pytest-mock",
    "pypi",
    "haha",
    "pip",
    "docker"
]


def is_multi_lang(lang):
    """Tests if input is a list."""
    return isinstance(lang, list)


class GoogleTranslate(commands.Cog):
    """Main class for googletrans"""
    def __init__(self, bot):
        """
        Here we innit the bot, the translator object, the language list,
        and our acceptable threshold
        """
        self.bot = bot
        self.gl = googletrans.LANGUAGES
        self.translator = Translator()
        self.threshold = 0.70

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Scans every message for non-english content.
        """
        if message.author.bot:
            return

        if message.content.lower() in whitelist:
            return

        if len(message.content) < 7:
            return

        detected = self.translator.detect(message.content)
        multi_lang = is_multi_lang(detected.lang)

        if 'en' in detected.lang:
            # If the message is english 70% english, just stop
            return


        logger.info("A message by %s was translated.", message.author.name)
        if multi_lang:
            lang = detected.lang[0].lower()
            lang_2 = detected.lang[1].lower()
            confidence = detected.confidence[0]  # extract value from confidence list
            detected_language = f'{self.gl[lang]}, {self.gl[lang_2]}'

        else:
            lang = detected.lang.lower()
            confidence = detected.confidence
            detected_language = f'{self.gl[lang]}'

        # translate message
        translation = self.translator.translate(message.content, dest='en')

        # send results of translation as embed
        embed = discord.Embed(
            title=f'{message.content}:',
            description=f'{translation.text}')

        embed.set_footer(text=f"translated from {detected_language}\nconfidence: {confidence * 100}%")
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
                title=f'{text}:',
                description=translated.text
            )
            embed.set_footer(text=f'translated from {self.gl[source_language]}')
            await ctx.respond(embed=embed)

        except ValueError as v:
            languages = ''
            for key, value in self.gl.items():
                languages += f'{key}: {value}\n'
            embed = discord.Embed(
                title='Valid Language Codes:',
                description=languages
            )
            embed.set_footer(text='''Please use the code on the left
    to select the language on the right''')
            await ctx.respond(embed=embed)


def setup(bot):
    """Docstrings4lyfe"""
    bot.add_cog(GoogleTranslate(bot))
