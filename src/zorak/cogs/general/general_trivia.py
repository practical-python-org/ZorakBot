"""
A trivia command.
"""
import logging
import json
from discord.ui.item import Item
import requests
import urllib
import html
from discord.ext import commands
import discord
import random
logger = logging.getLogger(__name__)

class GeneralTrivia(commands.Cog):
    """
    # Hits the trivia API and returns the response
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def trivia_cmd(self, ctx):
        """
        Sends a trivia using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        req = requests.get("https://opentdb.com/api.php?amount=1&category=18&difficulty=medium&type=multiple")
        if req.json()['response_code'] == 0:
            
            await ctx.respond(html.unescape(req.json()['results'][0]['question']))
            view = discord.ui.View()
            answer_list = []
            for i in req.json()['results'][0]['incorrect_answers']:
                answer_list.append((i,False))
            answer_list.append((req.json()['results'][0]['correct_answer'],True))
            al = answer_list[:]
            correct_ans = len(answer_list)-1
            button_list = []
            async def empty(interaction:discord.Interaction):
                pass
            async def correct(interaction:discord.Interaction):
                if interaction.user == ctx.author:
                    await interaction.response.defer()
                    await interaction.followup.send(content="The answer is correct, good job human")
                    for i in button_list:
                        i.callback = empty

            async def wrong(interaction:discord.Interaction):
                if interaction.user == ctx.author:
                    await interaction.response.defer()
                    await interaction.followup.send(content=f"Wrong answer, the answer was {answer_list[correct_ans][0]}")
                    await interaction.edit_original_response()
                    for i in button_list:
                        i.callback = empty
            for i in range(correct_ans+1):
                index = random.randint(0,len(al)-1)
                label = html.unescape(al[index][0])
                button = discord.ui.Button(label=label)
                button_list.append(button)
                #print(button.callback)
                if al[index][1]:
                    
                    button.callback = correct
                else:
                    button.callback = wrong
                del al[index]
                view.add_item(button)
            msg = await ctx.send(view=view)

        else:
            await ctx.respond('Oops the server seems to have made a mistake, try the command again')



def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralTrivia(bot))
