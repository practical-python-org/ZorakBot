import logging
import os
import toml
import json


logger = logging.getLogger(__name__)


class Settings:
    def __init__(self, settings_path, all_guilds):

        if all_guilds is None:
            logger.warning("Settings were triggered, but bot has no guilds!")
            return


        # self.settings_path = os.path.join(settings_path, "FAKE_DB_settings.json")
        self.reactions_path = os.path.join(settings_path, "reaction_roles.toml")
        self.reactions_path = os.path.join(settings_path, "reaction_roles.toml")
        self.verification_path = os.path.join(settings_path, "verification_options.toml")


        # with open(self.settings_path, 'r') as f:
        #     server_settings = json.load(f)
        #     self.server = server_settings


        # Reaction Roles
        try:
            self.reaction_role_data = toml.load(self.reactions_path)
        except Exception as e:
            self.reaction_role_data = None
            logger.warning(f"Failed to grab reaction roles. No file under {self.reactions_path}")

        # Verification Options
        try:
            self.verification_options = toml.load(self.verification_path)

        except Exception as f:
            logger.warning(f"Failed to grab verification options. No file under {self.reactions_path}")
            self.verification_options = None
