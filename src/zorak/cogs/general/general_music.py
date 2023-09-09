import asyncio

from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from yt_dlp import YoutubeDL

PREV_QUEUE_LIMIT = 10


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}  # A dictionary to hold queues for different guilds
        self.prev_songs = {}  # A dictionary to hold the last PREV_QUEUE_LIMIT 10 songs played in a guild

    # command for bot to join the channel of the user,
    # if the bot has already joined and is in a different channel, it will move to the channel the user is in
    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.command()
    async def skip(self, ctx):
        """Skip the current song and play the next song in the queue."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        if ctx.guild.id in self.queue and self.queue[ctx.guild.id]:
            last_played = self.queue[ctx.guild.id].pop(0)
            next_url = self.queue[ctx.guild.id][0]
            await self.play_song(ctx, next_url)
        else:
            voice.stop()

    async def play_song(self, ctx, url):
        """Play a song given its URL."""
        YDL_OPTIONS = {"format": "bestaudio/best[height<=480]", "noplaylist": "True"}
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info["url"]
        FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

        # Going for a callback approach, could also try state-machine and backround queue manager approaches
        def after_callback(error):
            if error:
                print(f"Player error: {error}")
            if ctx.guild.id in self.queue and self.queue[ctx.guild.id]:
                last_played = self.queue[ctx.guild.id].pop(0)
                next_url = self.queue[ctx.guild.id][0]
                # enqueue the last played song to the front of the played songs stack
                if ctx.guild.id not in self.prev_songs:
                    self.prev_songs[ctx.guild.id] = []
                if len(self.prev_songs[ctx.guild.id]) >= PREV_QUEUE_LIMIT:
                    self.prev_songs[ctx.guild.id].pop(0)  # Remove the oldest song if the limit is reached
                self.prev_songs[ctx.guild.id].append(url)
                asyncio.run_coroutine_threadsafe(self.play_song(ctx, next_url), self.bot.loop)

        await ctx.send(f"Playing: {url}")
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=after_callback)

    @commands.command()
    async def play(self, ctx, url):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        # Join the voice channel if the bot isn't already in one
        if not voice or (voice and not voice.is_connected()):
            await self.join(ctx)
            voice = get(self.bot.voice_clients, guild=ctx.guild)  # Re-fetch the voice client after joining

        # if len(self.queue.get(ctx.guild.id, [])) >= QUEUE_LIMIT:
        #     await ctx.send(f"Queue limit reached: ({QUEUE_LIMIT}), please wait for the queue to clear before adding more songs.")
        # else:
        if ctx.guild.id not in self.queue:
            self.queue[ctx.guild.id] = []
        self.queue[ctx.guild.id].append(url)

        if not voice.is_playing():
            await self.play_song(ctx, self.queue[ctx.guild.id][0])

    @commands.command()
    async def prev(self, ctx):
        """Play the previous song."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        if ctx.guild.id in self.prev_songs and self.prev_songs[ctx.guild.id]:
            prev_url = self.prev_songs[ctx.guild.id].pop()  # Get the last played song
            if ctx.guild.id in self.queue:
                self.queue[ctx.guild.id].insert(0, prev_url)  # Add the previous song to the start of the queue
            else:
                self.queue[ctx.guild.id] = [prev_url]
            await self.play_song(ctx, prev_url)
        else:
            await ctx.send("No previous song to play!")

    # command to resume voice if it is paused
    @commands.command()
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            await ctx.send("Resuming stream")

    # command to pause voice if it is playing
    @commands.command()
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.send("Paused stream")

    # command to stop voice
    @commands.command()
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            await ctx.send("Stopping stream...")

    @commands.command()
    async def clear_queue(self, ctx):
        self.queue[ctx.guild.id] = []
        await ctx.send("Queue cleared!")

    # async def youtube_video_autocompletion(self, ctx: AutocompleteContext):
    #     current = ctx.options["video"]
    #     data = []

    #     # Check if the current input is a link
    #     is_link = is_youtube_link(current)
    #     if is_link:
    #         return [current]  # Return the link as the only option

    #     # Otherwise, search YouTube for videos with the current string
    #     videos_search = VideosSearch(current, limit=5)
    #     results = videos_search.result()

    #     for video in results["result"]:
    #         video_link = video["link"]
    #         data.append(video_link)

    #     return data

    # @commands.slash_command()
    # async def play(
    #     self,
    #     ctx: ApplicationContext,
    #     video_name: Option(str, autocomplete=youtube_video_autocompletion),
    # ):
    #     YDL_OPTIONS = {"format": "bestaudio/best[height<=480]", "noplaylist": "True"}
    #     voice = get(self.bot.voice_clients, guild=ctx.guild)

    #     if is_youtube_link(video_name):
    #         url = video_name
    #     else:
    #         videos_search = VideosSearch(video_name, limit=5)
    #         results = videos_search.result()
    #         url = results["result"][0]["link"]

    #     if not voice.is_playing():
    #         with YoutubeDL(YDL_OPTIONS) as ydl:
    #             info = ydl.extract_info(url, download=False)
    #         voice.play(
    #             FFmpegPCMAudio(
    #                 info["url"], **{"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
    #             )
    #         )
    #         voice.is_playing()
    #         await ctx.send(f"Playing! {url}")

    #     # check if the bot is already playing
    #     else:
    #         await ctx.send("Bot is already playing! Please Stop it first with /stop")
    #         return


def setup(bot):
    bot.add_cog(Music(bot))
