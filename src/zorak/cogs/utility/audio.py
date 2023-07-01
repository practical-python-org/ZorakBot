import asyncio

import discord
import youtube_dl
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]
        filename = data["title"] if stream else ytdl.prepare_filename(data)
        return filename


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="join", help="Tells the bot to join the voice channel")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(self, ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.slash_command(name="leave", help="To make the bot leave the voice channel")
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.slash_command(name="play_song", help="To play song")
    async def play(self, ctx, url):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=self.bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send("**Now playing:** {}".format(filename))
        except:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.slash_command(name="pause", help="This command pauses the song")
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.slash_command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.slash_command(name="stop", help="Stops the song")
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
