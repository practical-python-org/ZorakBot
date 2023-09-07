import discord.ext
import googletrans
from discord.ext import commands
from googletrans import Translator

class googletrans_func(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):

		# default values
		THRESHOLD = 0.85 # confidence threshold
		multi_lang = False # check if detect() returns list

		try:
			if message.author.bot: return
			translator = Translator()
			detected = translator.detect(message.content)
			lang, confidence = detected.lang, detected.confidence
			# if detection picks up 2 potential languages
			if isinstance(lang, list):
				multi_lang = True
				confidence = confidence[0] # extract value from confidence list
				lang, lang_2 = lang[0], lang[1] # extract both langs
			# if english or less than 80% sure its not english & not > 1 language
			if lang == 'en' or confidence < THRESHOLD and not multi_lang: return
			if lang == 'zh-CN': lang = 'zh-cn' # fix bc the dict keys dont match
			# translate message
			translation = translator.translate(message.content, dest='en')
			gl = googletrans.LANGUAGES # googletrans dictionary of languages
			if multi_lang: detected_language = f'{gl[lang]}, {gl[lang_2]}'
			else: detected_language = f'{gl[lang]}'
			# send results of translation as embed
			embed = discord.Embed(
				title=f'{message.content}:',
				description=f'{translation.text}')
			embed.set_footer(text=f'''
translated from {detected_language}
confidence: {confidence * 100}%''')
			await message.channel.send(embed=embed)
		# if error, send error message to channel that caused it
		except Exception as e:
			print(e) # TODO: add pipe to zorak error cog (idk what it is lol sry)

	@commands.slash_command()
	async def translate(self, ctx, langauge, message):
		try:
			gl = googletrans.LANGUAGES
			translator = Translator()
			translated = translator.translate(message, dest=langauge)
			embed = discord.Embed(
				title=f'{message}:',
				description=translated.text
			)
			embed.set_footer(text=f'translated from {gl[langauge]}')
			await ctx.respond(embed=embed)
		except ValueError as v:
			languages = ''
			for key, value in gl.items():
				languages += f'{key}: {value}\n'
			embed = discord.Embed(
				title='Valid Language Codes:',
				description=languages
			)
			embed.set_footer(text='''Please use the code on the left
to select the language on the right''')
			await ctx.send(embed=embed)
		except Exception as e:
			print(e) # TODO: add pipe to zorak error cog (idk what it is lol sry)

def setup(bot):
	bot.add_cog(googletrans_func(bot))
