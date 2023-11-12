import logging
import os

import toml

logger = logging.getLogger(__name__)


class Settings:
    def __init__(self, settings_path):
        server_settings_path = os.path.join(settings_path, "channel_info.toml")
        try:
            server_settings = toml.load(server_settings_path)

            # Server
            self.server_info = server_settings["server"]["info"]

            # Channels
            self.channels = server_settings["channels"]
            self.mod_channel = self.channels["moderation"]
            self.log_channel = self.channels["log_channel"]
            self.normal_channel = self.channels["normal_channel"]

            # Roles
            self.user_roles = server_settings["user_roles"]
            self.admin_roles = self.user_roles["admin"]
            self.elevated_roles = self.user_roles["elevated"]
            self.badboi_role = self.user_roles["bad"]
            self.verified_role = self.user_roles["verified"]
            self.fun_roles = self.user_roles["fun"]
            self.employment_roles = self.user_roles["employment"]

            # RSS Feeds
            self.feeds = server_settings["rss_feeds"]
            self.rss_feed = self.feeds["links"]
        except Exception as e:
            logger.warning(f"Failed to grab server info. No file under {server_settings_path}")
            self.server_info = None
            self.channels = None
            self.mod_channel = None
            self.log_channel = None
            self.normal_channel = None
            self.user_roles = None
            self.admin_roles = None
            self.elevated_roles = None
            self.badboi_role = None
            self.verified_role = None
            self.fun_roles = None
            self.employment_roles = None
            self.feeds = None
            self.rss_feed = None

        reaction_role_config_path = os.path.join(settings_path, "reaction_roles.toml")
        try:
            self.reaction_role_data = toml.load(reaction_role_config_path)
        except Exception as e:
            self.reaction_role_data = None
            logger.warning(f"Failed to grab reaction roles. No file under {reaction_role_config_path}")
