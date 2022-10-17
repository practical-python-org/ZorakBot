import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from io import BytesIO
import datetime
import json
import logging
import pytz
import requests

requests.packages.urllib3.disable_warnings()

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Don't talk to me, I am being developed!", reference=ctx.message)

    @commands.command()
    async def taunt(self, ctx):
        taunt = BeautifulSoup(requests.get("https://fungenerators.com/random/insult/shakespeare/").content, "html.parser").find("h2")
        await ctx.send(taunt.text, reference=ctx.message)

    @commands.command()
    async def catfact(self, ctx):
        await ctx.send(json.loads(requests.get("https://catfact.ninja/fact").text)["fact"], reference=ctx.message)

    @commands.command()
    async def dogfact(self, ctx):
        await ctx.send(json.loads(requests.get("https://dog-api.kinduff.com/api/facts").text)["facts"][0], reference=ctx.message)

    @commands.command()
    async def pugfact(self, ctx):
        await ctx.send(
            BeautifulSoup(requests.get("https://fungenerators.com/random/facts/dogs/pug").content, "html.parser").find("h2").text[:-15],
            reference=ctx.message,
        )

    @commands.command()
    async def catpic(self, ctx):
        await ctx.send(
            file=discord.File(fp=BytesIO(requests.get("https://cataas.com/cat").content), filename="cat.png"), reference=ctx.message
        )

    @commands.command()
    async def joke(self, ctx):
        await ctx.send(
            json.loads(requests.get("https://geek-jokes.sameerkumar.website/api?format=json").text)["joke"], reference=ctx.message
        )

    @commands.command()
    async def quote(self, ctx):
        quote = json.loads(requests.get("https://zenquotes.io/api/random").text)[0]
        await ctx.send((quote["q"] + "\n- " + quote["a"]), reference=ctx.message)

    @commands.command()
    async def fakeperson(self, ctx):
        person = json.loads(requests.get("https://randomuser.me/api/").text)["results"]
        name = "Name: {} {} {}".format(person[0]["name"]["title"], person[0]["name"]["first"], person[0]["name"]["last"])
        hometown = "Hometown: {}, {}".format(person[0]["location"]["city"], person[0]["location"]["country"])
        age = "Age: {} Years old".format(person[0]["dob"]["age"])
        await ctx.send("You have requested a fake person:\n\n" + name + "\n" + hometown + "\n" + age, reference=ctx.message)

    @commands.command()
    async def google(self, ctx, *, args):
        await ctx.send(
            f"Here, allow me to google that one for you:\nhttps://letmegooglethat.com/?q={args.replace(' ', '+')}", reference=ctx.message
        )

    @commands.command()
    async def pokedex(self, ctx, *, pokemon):
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}")
        if data.status_code == 200:
            data = data.json()
            embed = discord.Embed(title=data["name"].title(), color=discord.Color.blue())
            embed.set_thumbnail(url=data["sprites"]["front_default"])
            embed.add_field(name="Stats", value=data["name"].title())
            embed.add_field(name="Weight", value=data["weight"])
            embed.add_field(name="Type", value=data["types"][0]["type"]["name"].title())
            embed.add_field(name="Abilities", value=data["abilities"][0]["ability"]["name"])
            return embed
        elif data.status_code == 404:
            embed = discord.Embed(title="Uhh oh...", color=discord.Color.blue())
            embed.set_thumbnail(url="https://assets.pokemon.com/assets/cms2/img/misc/gus/buttons/logo-pokemon-79x45.png")
            embed.add_field(name="Error", value=pokemon.title() + " does not exist!")
        await ctx.send(embed=embed)

    @commands.command()
    async def dogpic(self, ctx, *, breed=None):
        embed = discord.Embed(title="Dog Pic!", description="A lovely dog pic just for you.")
        if breed is None:
            link = requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
        elif breed is not None:
            link = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random").json()["message"]
        embed.set_image(url=link)
        await ctx.send(embed=embed)

    @commands.command()
    async def devtimes(
        self, ctx
    ):  # again, dict mapping could be good to help here, could also provide a command with timezone as input. Could do a whole times cog probably.
        tz_india = datetime.now(tz=pytz.timezone("Asia/Kolkata"))
        tz_japan = datetime.now(tz=pytz.timezone("Asia/Tokyo"))
        tz_america_ny = datetime.now(tz=pytz.timezone("America/New_York"))
        tz_austria = datetime.now(tz=pytz.timezone("Europe/Vienna"))
        tz_uk = datetime.now(tz=pytz.timezone("GMT"))
        times = (
            f"Japan (Chiaki): {tz_japan.strftime('%m/%d/%Y %I:%M %p')}",
            f"\nIndia (777advait): {tz_india.strftime('%m/%d/%Y %I:%M %p')}",
            f"\nAustria (Xarlos): {tz_austria.strftime('%m/%d/%Y %I:%M %p')}",
            f"\nAmerica (Minus): {tz_america_ny.strftime('%m/%d/%Y %I:%M %p')}",
            f"\nUK (Maszi): {tz_uk.strftime('%m/%d/%Y %I:%M %p')}",
        )
        embed = discord.Embed(title=f"**TIMES**", description="")
        embed.add_field(name="Staff", value=times)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FunCog(bot))
