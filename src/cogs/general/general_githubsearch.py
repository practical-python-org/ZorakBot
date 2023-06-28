"""
Searches github for a repo
"""
import logging
import requests
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class GithubSearch(commands.Cog):
    """Searches github for a repo"""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Search Github for a repo.")
    async def github_search(self, ctx, username, repo):
        """
        Searches GitHub for a specific repo.
        """
        logger.info("%s used the %s command."
                    , ctx.author.name
                    , ctx.command)
        try:
            info = requests.get(
                f"https://api.github.com/repos/{username}/{repo}"
                , timeout=5
            ).json()
            contrib_info = requests.get(
                f"https://api.github.com/repos/{username}/{repo}/contributors"
                , timeout=5
            ).json()
            embed = discord.Embed(
                title=info["name"],
                description=f"[Repository Link]({info['html_url']})",
                colour=discord.Colour.green(),
            )

            embed.add_field(name="Owner", value=info["owner"]["login"])
            embed.add_field(name="Language", value=info["language"])
            embed.add_field(name="Stars", value=info["stargazers_count"])
            embed.add_field(name="Forks", value=info["forks"])
            embed.add_field(
                name="License",
                value=info["license"]["name"]
                if info["license"] is not None
                else "None",
            )
            embed.add_field(name="Open Issues", value=info["open_issues"])
            embed.add_field(
                name="Contributors",
                value="\n".join([contribs["login"] for contribs in contrib_info]),
            )
            embed.set_thumbnail(url=info["owner"]["avatar_url"])
            await ctx.respond(embed=embed)

        except ValueError:
            embed = discord.Embed(
                title="Oops",
                description=f"Repository {username}/{repo} does not exist.",
                colour=discord.Colour.red(),
            )
            await ctx.respond(embed=embed)


def setup(bot):
    """Required."""
    bot.add_cog(GithubSearch(bot))
