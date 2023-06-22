"""
This file holds all the discord embeds for the entire application.
this is to clean up the cogs, and allow these embeds to be viewed
in one place.
"""
from datetime import datetime
import discord


def embed_avatar(before, after):
    """
    Embedding for avatar change alerts.
    """
    embed = discord.Embed(
        title=f'{before} updated their profile picture!'
        , color=discord.Color.dark_grey()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=after.avatar
    )

    return embed


def embed_ban(some_member, audit_log_entry):
    """
    Embedding for user ban alerts.
    """
    embed = discord.Embed(
        title=f'<:red_circle:1043616578744357085> {some_member} was banned'
        , description=f'By: {audit_log_entry.user}'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name='Reason:'
        , value=f'{audit_log_entry.reason}'
        , inline=True
    )

    return embed


def embed_kick(some_member, audit_log_entry):
    """
    Embedding for user kick alerts.
    """
    embed = discord.Embed(
        title=f'<:red_circle:1043616578744357085> {some_member} was kicked'
        , description=f'By: {audit_log_entry.user}'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name='Reason:'
        , value=f'{audit_log_entry.reason}'
        , inline=True
    )
    return embed


def embed_leave(some_member):
    """
    Embedding for user leave alerts.
    """
    embed = discord.Embed(
        title='\u200b'
        , description=f'{some_member} has left us.'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    return embed


def embed_message_delete(some_member, some_author, some_message):
    """
    Embedding for user message deletion alerts.
    """
    embed = discord.Embed(
        title='<:red_circle:1043616578744357085> Deleted Message'
        , description=f'{some_author} deleted a message'
                      f'\nIn {some_message.channel}\nMessage '
                      f'author: {some_message.author}'
        , color=discord.Color.dark_red()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=some_member.avatar
    )
    if len(some_message.content) > 1020:
        the_message = some_message.content[0:1020] + '...'
    else:
        the_message = some_message.content
    embed.add_field(
        name='Message: '
        , value=the_message
        , inline=True
    )

    return embed


def embed_message_edit(some_username, orig_author, some_message_before, some_message_after):
    """
    Embedding for user message edit alerts.
    """
    embed = discord.Embed(
        title='<:orange_circle:1043616962112139264> Message Edit'
        , description=f'Edited by {some_username}\n'
                      f'In {some_message_after.channel.mention}'
        , color=discord.Color.dark_orange()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=orig_author.avatar
    )

    embed.add_field(
        name='Original message: '
        , value=some_message_before.content
        , inline=True
    )

    embed.add_field(
        name="After editing: "
        , value=some_message_after.content
        , inline=True
    )

    return embed


def embed_name_change(name_before, name_after, username_before, username_after):
    """
    Embedding for user name change alerts.
    """
    embed = discord.Embed(
        title='<:grey_exclamation:1044305627201142880> Name Change'
        , description=f'Changed by: {name_before}.'
        , color=discord.Color.dark_grey()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=name_after.avatar
    )

    embed.add_field(
        name='Before'
        , value=username_before
        , inline=True
    )

    embed.add_field(
        name='After'
        , value=username_after
        , inline=True
    )

    return embed


def embed_verified_success(name, amount):
    """
    Embedding for user verification success, and therefore a join
    """
    embed = discord.Embed(
        title="",
        description=f"{name}, human number {amount} has joined.",
        color=discord.Color.dark_green(),
    )

    return embed


def embed_ticket_create(user, ticket_name):
    """
    Embed for creation of a new ticket.
    """
    embed = discord.Embed(
        title=f"{str(user)} opened a ticket.",
        description=f"Ticket: {ticket_name}",
        color=discord.Color.green(),
        timestamp=datetime.utcnow(),
    )

    return embed


def embed_ticket_update(user, ticket_name):
    """
    Embed for update of a new ticket.
    """
    embed = discord.Embed(
        title=f"{str(user)} updated a ticket.",
        description=f"Ticket: <#{ticket_name}>",
        color=discord.Color.green(),
        timestamp=datetime.utcnow(),
    )

    return embed


def embed_ticket_delete(user, ticket_name):
    """
    Embed for deletion of a new ticket.
    """
    embed = discord.Embed(
        title=f"{str(user)} deleted a ticket.",
        description=f"Ticket: <#{ticket_name}>",
        color=discord.Color.red(),
        timestamp=datetime.utcnow(),
    )

    return embed


def embed_ticket_remove(user, ticket_name):
    """
    Embed for removal of a new ticket.
    """
    embed = discord.Embed(
        title=f"{str(user)} removed a ticket.",
        description=f"Ticket: <#{ticket_name}>",
        color=discord.Color.red(),
        timestamp=datetime.utcnow(),
    )

    return embed


def embed_unban(some_member):
    """
    Embedding for user un-ban alerts.
    """
    embed = discord.Embed(
        title='<:green_circle:1046088647759372388> User Un-Banned'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name=f'{some_member.name} was un-banned.'
        , value='Welcome back.'
        , inline=True
    )

    return embed


def embed_role_add(some_member, member_who_did_action, role_obj):
    """
    Embedding for user kick alerts.
    """
    embed = discord.Embed(
        title=':green_square: Role Update'
        , description=f'<@{member_who_did_action.id}> added a role to <@{some_member.id}> '
        , color=discord.Color.green()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name='Added role:'
        , value=f'<@&{role_obj.id}>'
        , inline=True
    )
    return embed


def embed_role_remove(some_member, member_who_did_action, role_obj):
    """
    Embedding for user kick alerts.
    """
    embed = discord.Embed(
        title=f':negative_squared_cross_mark: Role Update'
        , description=f'<@{member_who_did_action.id}> removed a role from <@{some_member.id}>'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name='Removed role:'
        , value=f'<@&{role_obj.id}>'
        , inline=True
    )
    return embed


def embed_definition(the_word, part_of_speech, definition, synonym, source):
    """
    Embedding for /define command
    """
    embed = discord.Embed(
        title=the_word.capitalize()
        , description=f'**{part_of_speech.capitalize()}**\n{definition}'
        , color=discord.Color.green()
    )
    if synonym is not None:
        embed.add_field(
            name='Synonym'
            , value=synonym.capitalize()
            , inline=True
        )
    embed.add_field(
        name=''
        , value=f"[Source]({source})"
        , inline=True
    )
    return embed



