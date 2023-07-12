"""
A simple command that shows info on a Pokemon
"""
import logging
import requests
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class GeneralPokedex(commands.Cog):
    """
    # Hits the pokeapi API and returns the response.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def pokedex(self, ctx, pokemon):
        """
        Sends pokemon information using an API
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        data = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
            , timeout=5)
        if data.status_code == 200:
            data = data.json()
            embed = discord.Embed(
                title=data["name"].title(), color=discord.Color.blue()
            )
            embed.set_thumbnail(url=data["sprites"]["front_default"])
            embed.add_field(name="Stats", value=data["name"].title())
            embed.add_field(name="Weight", value=data["weight"])
            embed.add_field(name="Type", value=data["types"][0]["type"]["name"].title())
            embed.add_field(
                name="Abilities", value=data["abilities"][0]["ability"]["name"]
            )
            await ctx.respond(embed=embed)
        elif data.status_code == 404:
            embed = discord.Embed(title="Uhh oh...", color=discord.Color.blue())
            embed.set_thumbnail(
                url="https://assets.pokemon.com/assets/cms2/img/misc/gus/buttons"
                    "/logo-pokemon-79x45.png"
            )
            embed.add_field(name="Error", value=pokemon.title() + " does not exist!")
            await ctx.respond(embed=embed)


def setup(bot):
    """
    Required.
    """
    bot.add_cog(GeneralPokedex(bot))
