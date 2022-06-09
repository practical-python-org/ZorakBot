"""
The MIT License (MIT)

Copyright (c) 2021-2021 GreenDiscord

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


import discord

import random

__version__ = '0.0.2-a'


def randemoji():
    emoji = ["XwX", "OvO", "OwO", "UwU", ">:3", "-w-", "ÙwÚ", "CwC"]
    return f"{random.choice(emoji)}"


async def owoify(text):
    """
    Owoify's given text
    You need to await this function.
    """
    message = text.replace("r", "w").replace(
        "l", "w").replace("L", "W").replace("R", "W")
    owoified = f"{message} {randemoji()}"
    return owoified


async def owo():
    """
    Returns random owo emoji
    You need to await this function.
    """
    return randemoji()


async def discord_owo(channel, text):
    """
    Sends owoified message to a certain channel
    Please use "owoify" for other uses
    You need to await this function.
    """
    message = text.replace("r", "w").replace(
        "l", "w").replace("L", "W").replace("R", "W")
    owoified = f"{message} {randemoji()}"
    return await channel.send(f"{owoified}")


async def user_owo(channel, text, name):
    """
    Owoifys a users text for a user
    You need to use await for this function
    """
    message = text.replace("r", "w").replace(
        "l", "w").replace("L", "W").replace("R", "W")
    return await channel.send(f"{message} - {name}")


async def decode(text):
    decoded = text.replace("hewwo", "hello").replace("Hewwo", "Hello").replace(
        "Wuve", "Love").replace("wuve", "love").replace("Awe", "Are").replace("awe", "are")
    return decoded
