#!/usr/bin/env python3

# This example requires the 'message_content' intent.
import discord
import asyncio
import time
import os

# optional: try to load .env locally; in docker, env comes from .env file anyway
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ── CONFIGURATION ────────────────────────────────────────────────────────────
DISBOARD_BOT_ID  = int(os.getenv("DISBOARD_BOT_ID", 0))
# BOT_TOKEN      = os.getenv("BOT_TOKEN")    # not used inside Zorak
BUMP_CHANNEL_ID  = int(os.getenv("BUMP_CHANNEL_ID", 0))
BUMP_ROLE_ID     = int(os.getenv("BUMP_ROLE_ID", 0))
CHECK_INTERVAL   = 60
BUMP_INTERVAL    = 7200
# TEST_USER_ID =    #for testing fake bump

from discord.ext import commands, tasks

class BumpReminder(commands.Cog):
    """
    Your bump reminder, as a Cog.
    - watches for DISBOARD 'Bump done'
    - after BUMP_INTERVAL, pings the role in BUMP_CHANNEL_ID
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_bump = 0
        self._reminder_loop.start()   # start the background loop

    def cog_unload(self):
        self._reminder_loop.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[bump] Cog loaded as {self.bot.user}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ── FAKE-BUMP TRIGGER (for testing only) ────────────
        # if message.author.id == TEST_USER_ID and message.content.lower() == "!fakebump":
        #     self.last_bump = time.time()
        #     print("🧪  Simulated bump at", time.ctime(self.last_bump))
        #     return                    # skip the rest
        # ────────────────────────────────────────────────────
        if not message.guild or message.author.id != DISBOARD_BOT_ID:
            return

        text = (message.content or "").lower()
        if message.embeds:
            e0 = message.embeds[0].to_dict()
            text += " " + (e0.get("title") or "").lower()
            text += " " + (e0.get("description") or "").lower()

        if "bump done" in text:
            self.last_bump = time.time()
            print("✅  Registered bump at", time.ctime(self.last_bump))

    @tasks.loop(seconds=CHECK_INTERVAL)
    async def _reminder_loop(self):
        # run every CHECK_INTERVAL seconds
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(BUMP_CHANNEL_ID)
        if not isinstance(channel, discord.TextChannel):
            # print only once per process start if you want; keeping it quiet
            return

        if self.last_bump and (time.time() - self.last_bump) >= BUMP_INTERVAL:
            await channel.send(f"<@&{BUMP_ROLE_ID}> Time to bump again!")
            self.last_bump = 0  # wait for next bump

# Zorak loader hook
async def setup(bot: commands.Bot):
    await bot.add_cog(BumpReminder(bot))