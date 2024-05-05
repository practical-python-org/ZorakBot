# pylint: skip-file
"""
Archived, non-working commands that should be worked on and
brought back into this world
"""
import math

# import datetime
# import discord
# from discord.ext import commands
# from pistonapi import PistonAPI
# import requests
# import pytz


# # TODO: Hitting an import error in LaTeX
# # AttributeError: module 'matplotlib.pyplot' has no attribute 'mathtext'
#     @commands.slash_command(description='Sends a latex image.')
#     async def latex(self, ctx, expr: discord.Option(str)):
#         """
#         Sends a latex image of a formula.
#         """
#         plt.rcParams["savefig.transparent"] = True
#         plt.rcParams["text.color"] = "white"
#         buff = BytesIO()
#         plt.mathtext.math_to_image(
#             f"${expr}$".replace("\n", " "),
#             buff,
#             dpi=300,
#             prop=plt.font_manager.FontProperties(
#                 size=30
#                 , family="serif"
#                 , math_fontfamily="cm"),
#             format="png",
#         )
#         buff.seek(0)
#         embed = discord.Embed(colour=discord.Colour.green())
#         embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
#         embed.set_image(url="attachment://expr.png")
#         await ctx.respond(embed=embed, file=discord.File(fp=buff, filename="expr.png"))


# # TODO: Avatars. shit doesn't work.
# # Issue is with "discord.User.display_avatar"
# @commands.slash_command(description='Grabs the avatar of a user.')
# async def avatar(self, ctx, member: discord.Option(str)):
#     """
#     Sends the avatar of a user.
#     """
#     if member is 'me':
#         member = ctx.author
#     embed = discord.Embed(
#         title=f"Avatar for {member}",
#         description=f"[Download image]({discord.User.display_avatar})")
#     embed.set_image(url=discord.User.display_avatar)
#     await ctx.respond(embed=embed)


# # TODO: poll sends error
# # discord.errors.ApplicationCommandInvokeError:
# # Application Command raised an exception:
# # ValueError: too many values to unpack (expected 2)
#     @commands.slash_command()
#     async def poll(self, ctx, title, option1, option2, option3='', option4='', option5=''):
#         """
#         Makes a poll where people can vote for different items.
#         """
#         options = [option1,option2, option3,option4,option5]
#         reactions = ['1️⃣','2️⃣','3️⃣','4️⃣ ','5️⃣ ']
#         embed = discord.Embed(description=f"{title}")
#         for opt, num in options,reactions:
#             if opt != '':
#                 embed.add_field(name=num, value=opt, inline=False)
#         msg = await ctx.respond(embed=embed)
#         for idx, option in enumerate(options):
#             if option != '':
#                 await msg.add_reaction(reactions[str(idx)])


# # TODO: Does not see other members, only the author.
# # Figure out how to call up other users.
#     @commands.slash_command(description='Sends info about a user.')
#     async def whois(self, ctx, member: discord.User):
#         """
#         A user-lookup command that sends info about a user.
#         """
#         if member is None:
#             member = ctx.author
#
#         roles = list(self.bot.member.roles)
#         embed = discord.Embed(colour=discord.Colour.orange(), title=str(member.display_name))
#         # embed.set_thumbnail(url=member.avatar_url)
#         embed.set_footer(text=f"Requested by {ctx.author}")
#         embed.add_field(name="Username:", value=member.name, inline=False)
#         embed.add_field(name="ID:", value=member.id, inline=False)
#         embed.add_field(name="Account Created On:"
#                         , value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
#                         , inline=False)
#         embed.add_field(name="Joined Server On:"
#                         , value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
#                         , inline=False)
#         try:
#             embed.add_field(name="Roles:"
#                             , value="".join([role.mention for role in roles[1:]]))
#             embed.add_field(name="Highest Role:", value=member.top_role.mention)
#         except:
#             pass
#         await ctx.respond(embed=embed)
