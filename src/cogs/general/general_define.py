"""
searches a free API: https://api.dictionaryapi.dev/api/v2/entries/en/{word}
and returns the definition of a word
"""
import logging
import json
import requests
from discord.ext import commands

from utilities.cog_helpers._embeds import embed_definition  # pylint: disable=E0401


logger = logging.getLogger(__name__)


class Define(commands.Cog):
    """
    docstrings go brrrr
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def define(self, ctx, word):
        """
        hit the api
        make some vars
        make an embed
        handle the errors
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        data = json.loads(
            requests.get(
                f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
                , timeout=5
            ).content)

        if 'message' not in data:
            the_word = data[0]['word']
            part_of_speech = data[0]['meanings'][0]['partOfSpeech']
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            if len(data[0]['meanings'][0]['definitions'][0]['synonyms']) > 0:
                synonym = data[0]['meanings'][0]['definitions'][0]['synonyms'][0]
            else:
                synonym = None
            source = data[0]['sourceUrls'][0]

            await ctx.respond(
                embed=embed_definition(
                    the_word
                    , part_of_speech
                    , definition
                    , synonym
                    , source
                ))
        else:
            await ctx.respond(f"Sorry, could find '{word}'. Are you sure that's correct?")


def setup(bot):
    """
    linting is so fun.
    """
    bot.add_cog(Define(bot))
