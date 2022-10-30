import discord
from discord.ext import commands
from __main__ import bot

class helpButtons(discord.ui.View):
	async def on_timeout(self):
		for button in self.children:
			button.disabled = True
		await self.message.edit(view=self)

	@discord.ui.button(label="Ping", row=0, style=discord.ButtonStyle.success)
	async def first_button_callback(self, button, interaction):
		embed=discord.Embed(
			title="Pong!",
			description=f"Zorak's current ping is **{round(bot.latency*100)}**ms",
			color=discord.Color.green(),
		)
		await interaction.response.send_message(embed=embed)

	@discord.ui.button(label="Commands", row=0, style=discord.ButtonStyle.success)
	async def second_button_callback(self, button, interaction):
		help_msg = """
	  ***For-fun commands***
		  - /hello
		  - /catfact
		  - /dogfact
		  - /pugfact
		  - /quote
		  - /joke
		  - /8ball [question]
		  - /taunt
		  - /rolldice
		  - /owo [text]
		  - /catpic
		  - /dogpic [breed] (Optional)
		  - /pokedex [pokemon]
		  - /drawme arg:[text] arg:[seed]
				
	  ***Utility Commands***
		  - /codeblock
		  - /runcode
		  - /preview
		  - /google [question]
		  - /embed [title] [content]  
		  - /zeus [website]
		  - /fakeperson
		  - /poll [title] [options]
		  - /suggest [suggestion]
		  - /avatar [member] 
		  - /whois [member] (Optional)
		  - /pipsearch [package]
		  - /ping
		  - /github_search [endpoint]
	  """
		embed = discord.Embed(
		  title="User-Commands"
		  , description=help_msg)
		await interaction.response.send_message(embed=embed)
	
	@discord.ui.button(label="Running code", row=0, style=discord.ButtonStyle.success)
	async def third_button_callback(self, button, interaction):
		await interaction.response.send_message("""To run python code in the chat, type:\n \./run python \n\`\`\`py Your code here \`\`\`""")

	@discord.ui.button(label="Code Blocks", row=0, style=discord.ButtonStyle.success)
	async def fourth_button_callback(self, button, interaction):
		await interaction.response.send_message("""To format your python code like this: \n```py x = 'Hello World!' ``` Type this: \`\`\`py Your code here \`\`\`""")

class helper(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.slash_command(description='Various help topics.')# Create a slash command
	async def help(self, ctx):
		await ctx.respond("What do you want, earthling?", view=helpButtons(timeout=10))


def setup(bot):
	bot.add_cog(helper(bot))