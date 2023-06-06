from discord.ext import commands
from ._settings import log_channel, server_info


class LoggingRoles(commands.Cog):
    """
    Simple listener to on_member_update
    """
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        current_guild = self.bot.get_guild(server_info['id'])
        audit_log = [entry async for entry in current_guild.audit_logs(limit=1)][0]

        if str(audit_log.action) == 'AuditLogAction.member_role_update':
            print(audit_log)
            member = audit_log.target

            # This logic creates a list that contains the role that was changed.
            changed_roles = []
            if len(before.roles) > len(after.roles):
                for role in before.roles:
                    if role not in after.roles:
                        changed_roles.append(role)

            elif len(before.roles) < len(after.roles):
                for role in after.roles:
                    if role not in before.roles:
                        changed_roles.append(role)

            # TODO: Build the embed that takes in these values
            #   Send that embed to the mod_log channel
            for i in changed_roles:
                print(i.id) # gives us the ID of the role from the audit log
                print(i.name) # Gives us the string name of the role. <@{i.id}> to mention

                # # Here is a template of what's next, but I'm out of time for now.
                # embed = embed_kick(member, audit_log)
                #
                # logs_channel = await self.bot.fetch_channel(log_channel['mod_log'])
                # await logs_channel.send(embed=embed)




def setup(bot):
    """
    Necessary for loading the cog into the bot instance.
    """
    bot.add_cog(LoggingRoles(bot))
