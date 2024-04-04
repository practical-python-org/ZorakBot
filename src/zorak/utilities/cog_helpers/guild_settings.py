import logging


logger = logging.getLogger(__name__)


class GuildSettings():
    def __init__(self, settings, guild):
        self.settings = settings
        self.guild_name = guild
        self.guild_id = str(guild.id)
        self.guild_settings = self.settings[self.guild_id]

        if self.guild_id not in self.settings:
            logger.warning(f"No settings found for guild: {self.guild_id}")
        if self.guild_settings is None:
            logger.warning(f"No settings found for guild: {self.guild_id}")

        # All Channel information for guilds
        try:
            self.general_channels = self.guild_settings["channels"]["general"]  # has sub-channels
            self.quarantine_channel = self.guild_settings["channels"]["quarantine"]["quarantine_channel"]  # Explicit
            self.support_channel = self.guild_settings["channels"]["support"]["server_support"]  # Explicit
            self.verification_channel = self.guild_settings["channels"]["verification"]["verification_channel"]  # Explicit
        except Exception as e:
            logger.warning(f"Failed to grab channel info. Error: {e}")
            self.general_channels = None
            self.quarantine_channel = None
            self.support_channel = None
            self.verification_channel = None

        # All Logging channel information for guilds
        try:
            self.chat_log = self.guild_settings["channels"]["logging"]["chat_log"]
            self.error_log =self.guild_settings["channels"]["logging"]["zorak_log"]
            self.join_log = self.guild_settings["channels"]["logging"]["join_log"]
            self.mod_log =self.guild_settings["channels"]["logging"]["mod_log"]
            self.server_log =self.guild_settings["channels"]["logging"]["server_change_log"]
            self.user_log = self.guild_settings["channels"]["logging"]["user_log"]
            self.verification_log =self.guild_settings["channels"]["logging"]["verification_log"]
        except Exception as e:
            logger.warning(f"Failed to grab logging channels. Error: {e}")
            self.chat_log = None
            self.error_log = None
            self.join_log = None
            self.mod_log = None
            self.server_log = None
            self.user_log = None
            self.verification_log = None

        # All Role information for guilds
        try:
            self.admin_roles = self.guild_settings["roles"]["admin"]  # has sub-roles
            self.reaction_roles = self.guild_settings["roles"]["reaction"]  # has sub-roles
            self.punishment_role = self.guild_settings["roles"]["punishment"]["naughty"]  # explicit
            self.verified_role = self.guild_settings["roles"]["verified"]["verified"]  # explicit
        except Exception as e:
            logger.warning(f"Failed to grab role IDs. Error: {e}")
            self.admin_roles = None
            self.reaction_roles = None
            self.punishment_role = None
            self.verified_role = None

        # All General information for guilds
        try:
            self.info = self.guild_settings["info"]
        except Exception as e:
            logger.warning(f"Failed to grab server info. Error: {e}")
            self.info = None














