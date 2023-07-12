"""
Here we define TOML variables to be used throughout the cogs
TODO: Kill this shit off.
"""
import logging
import os

import toml

logger = logging.getLogger(__name__)

stage = os.getenv("SETTINGS")
logger.info("using settings at: {%s}", stage)

############
#  Server  #
############
server_info = toml.load(stage)["server"]["info"]

############
# Channels #
############
channels = toml.load(stage)["channels"]

mod_channel = channels["moderation"]
log_channel = channels["log_channel"]
normal_channel = channels["normal_channel"]

#############
#   Roles   #
#############
user_roles = toml.load(stage)["user_roles"]

admin_roles = user_roles["admin"]
elevated_roles = user_roles["elevated"]
badboi_role = user_roles["bad"]
unverified_role = user_roles["unverified"]
fun_roles = user_roles["fun"]
employment_roles = user_roles["employment"]

#############
# RSS Feeds #
#############
feeds = toml.load(stage)["rss_feeds"]

rss_feed = feeds["links"]
