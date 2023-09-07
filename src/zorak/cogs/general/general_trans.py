
import discord.ext
import googletrans
from discord.ext import commands
from googletrans import Translator


def is_multi_lang(lang):
    if isinstance(lang, list):
        return True
    else:
        return False


class googletrans_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gl = googletrans.LANGUAGES
        self.translator = Translator()
        self.threshhold = 0.85

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        detected = self.translator.detect(message.content)
        multi_lang = is_multi_lang(detected.lang)

        if 'en' in detected.lang and detected.confidence > self.threshhold:
            # If the message is english, just stop
            return

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
    async def translate(self, ctx, input_language, text):
        try:
            translated = self.translator.translate(text, dest=input_language)
            embed = discord.Embed(
                title=f'{text}:',
                description=translated.text
            )
            embed.set_footer(text=f'translated from {self.gl[input_language]}')
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
    bot.add_cog(googletrans_func(bot))
