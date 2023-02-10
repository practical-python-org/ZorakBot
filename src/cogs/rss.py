from asyncio import sleep
import discord
import feedparser
import html2text
from discord.ext import commands
from ._settings import normal_channel, rss_feed


class RSS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def rss_on_ready(self):
        def get_IDs():
            """Grabs the most recent article ID from each URL in
            the TOML, so that we can check what we have already sent"""
            most_recent_IDs = []

            for news_source in rss_feed.keys():
                news_feed = feedparser.parse(rss_feed[news_source])

                id_code = news_feed["entries"][0]["id"]
                most_recent_IDs.append(id_code)

            return most_recent_IDs

        def send_news(ID_to_send):
            """Uses the RSS ID's we grab from get_IDs that are NOT already in the DB.
            Sends out the news story if it is not in our DB.
            Each news story is parsed 'slightly' different, which is annoying."""

            def send_python_software_foundation(ID_tag):
                NewsFeed = feedparser.parse(rss_feed["Python_Software_foundation"])
                id_code = NewsFeed["entries"][0]["id"]
                if ID_tag == id_code:
                    # if the ID code in the article matches the ID we grabbed in get_IDs(), send.
                    html_reader = html2text.HTML2Text()
                    html_reader.ignore_links = False

                    embed = discord.Embed(
                        title=NewsFeed["entries"][0]["title"],
                        description=f"By: {NewsFeed['entries'][0]['authors'][0]['name']} at the Python Software Foundation!",
                        color=discord.Color.blue(),
                    )

                    embed.add_field(
                        name="Preview: ",
                        value=f"{html_reader.handle(NewsFeed['entries'][0]['summary'])[0:1015]} ...",
                        inline=False,
                    )

                    embed.add_field(
                        name="Read more: ",
                        value=f"[{NewsFeed['entries'][0]['link']}]({NewsFeed['entries'][0]['link']})",
                        inline=False,
                    )
                    embed.set_thumbnail(
                        url="https://www.python.org/static/img/python-logo@2x.png"
                    )

                    return embed
                else:
                    return

            def send_jetbrains(ID_tag):
                jetbrains = rss_feed["jetbrains"]
                NewsFeed = feedparser.parse(jetbrains)
                id_code = NewsFeed["entries"][0]["id"]
                if ID_tag == id_code:
                    # if the ID code in the article matches the ID we grabbed in get_IDs(), send.

                    html_reader = html2text.HTML2Text()
                    html_reader.ignore_links = False

                    # html = html_reader.handle(NewsFeed['entries'][0]['content'][0]['value'])

                    embed = discord.Embed(
                        title=f"**{NewsFeed['entries'][0]['title']}**",
                        description=f"By: **{NewsFeed['entries'][0]['author']}** at Jetbrains!",
                        color=discord.Color.blue(),
                    )

                    summary_text = f"{NewsFeed['entries'][0]['summary'][0:1015]} ..."
                    embed.add_field(
                        name="**Preview: **", value=summary_text, inline=False
                    )
                    embed.add_field(
                        name="**Read more: **",
                        value=f"[{NewsFeed['entries'][0]['link']}]({NewsFeed['entries'][0]['link']})",
                        inline=False,
                    )
                    embed.set_thumbnail(url=NewsFeed["entries"][0]["featuredimage"])
                    return embed
                else:
                    return

            embed = send_python_software_foundation(ID_to_send)
            embed2 = send_jetbrains(ID_to_send)
            if embed is not None:
                return embed
            else:
                return embed2

        while True:
            sent_ID_list = []

            all_ids = self.bot.db_client.get_all_stories()
            for ID in all_ids:
                sent_ID_list.append(ID)

            print(sent_ID_list)
            story_queue = get_IDs()

            for entry in story_queue:
                if entry not in sent_ID_list:
                    news_channel = await self.bot.fetch_channel(
                        normal_channel["news_channel"]
                    )

                    await news_channel.send(embed=send_news(entry))
                    self.bot.db_client.add_story_to_table(entry)

            wait_time_in_seconds = 86400  # 24 hour
            await sleep(wait_time_in_seconds)


def setup(bot):
    bot.add_cog(RSS(bot))
