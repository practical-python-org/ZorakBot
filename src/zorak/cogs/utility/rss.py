"""
Grabs info from an RSS feed, and posts it in the server.
"""
from asyncio import sleep

import discord
import feedparser
import html2text
from discord.ext import commands

from zorak.cogs import normal_channel, rss_feed  # pylint: disable=E0401


class RSS(commands.Cog):
    """
    The main class for the RSS handler.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def rss_on_ready(self):
        """
        This gets called to check if new stories are ready.
        """

        def get_ids():
            """Grabs the most recent article ID from each URL in
            the TOML, so that we can check what we have already sent"""
            most_recent_ids = []

            for news_source in rss_feed.keys():
                news_feed = feedparser.parse(rss_feed[news_source])

                id_code = news_feed["entries"][0]["id"]
                most_recent_ids.append(id_code)

            return most_recent_ids

        def send_news(id_to_send):
            """Uses the RSS ID's we grab from get_IDs that are NOT already in the DB.
            Sends out the news story if it is not in our DB.
            Each news story is parsed 'slightly' different, which is annoying."""

            def send_python_software_foundation(id_tag):
                newsfeed = feedparser.parse(rss_feed["Python_Software_foundation"])
                id_code = newsfeed["entries"][0]["id"]
                if id_tag == id_code:
                    # if the ID code in the article matches the ID we grabbed in get_IDs(), send.
                    html_reader = html2text.HTML2Text()
                    html_reader.ignore_links = False

                    embed = discord.Embed(
                        title=newsfeed["entries"][0]["title"],
                        description=f"By: {newsfeed['entries'][0]['authors'][0]['name']}" f" at the Python Software Foundation!",
                        color=discord.Color.blue(),
                    )

                    embed.add_field(
                        name="Preview: ",
                        value=f"{html_reader.handle(newsfeed['entries'][0]['summary'])[0:1015]}" f" ...",
                        inline=False,
                    )

                    embed.add_field(
                        name="Read more: ",
                        value=f"[{newsfeed['entries'][0]['link']}]" f"({newsfeed['entries'][0]['link']})",
                        inline=False,
                    )
                    embed.set_thumbnail(url="https://www.python.org/static/img/python-logo@2x.png")

                    return embed
                return None

            def send_jetbrains(id_tag):
                jetbrains = rss_feed["jetbrains"]
                newsfeed = feedparser.parse(jetbrains)
                id_code = newsfeed["entries"][0]["id"]
                if id_tag == id_code:
                    # if the ID code in the article matches the ID we grabbed in get_IDs(), send.

                    html_reader = html2text.HTML2Text()
                    html_reader.ignore_links = False

                    # html = html_reader.handle(NewsFeed['entries'][0]['content'][0]['value'])

                    embed = discord.Embed(
                        title=f"**{newsfeed['entries'][0]['title']}**",
                        description=f"By: **{newsfeed['entries'][0]['author']}** at Jetbrains!",
                        color=discord.Color.blue(),
                    )

                    summary_text = f"{newsfeed['entries'][0]['summary'][0:1015]} ..."
                    embed.add_field(name="**Preview: **", value=summary_text, inline=False)
                    embed.add_field(
                        name="**Read more: **",
                        value=f"[{newsfeed['entries'][0]['link']}]" f"({newsfeed['entries'][0]['link']})",
                        inline=False,
                    )
                    embed.set_thumbnail(url=newsfeed["entries"][0]["featuredimage"])
                    return embed
                return None

            embed = send_python_software_foundation(id_to_send)
            embed2 = send_jetbrains(id_to_send)
            if embed is not None:
                return embed
            return embed2

        while True:
            sent_id_list = []

            all_ids = self.bot.db_client.get_all_stories()
            for id_feed in all_ids:
                sent_id_list.append(id_feed)

            print(sent_id_list)
            story_queue = get_ids()

            for entry in story_queue:
                if entry not in sent_id_list:
                    news_channel = await self.bot.fetch_channel(normal_channel["news_channel"])

                    await news_channel.send(embed=send_news(entry))
                    self.bot.db_client.add_story_to_table(entry)

            wait_time_in_seconds = 86400  # 24 hour
            await sleep(wait_time_in_seconds)


def setup(bot):
    """required"""
    bot.add_cog(RSS(bot))
