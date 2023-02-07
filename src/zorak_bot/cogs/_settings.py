import toml

test = "./Resources/test_server.toml"
prod = "./Resources/server.toml"

# Set's the current stage throughout the TOML.
stage = test


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

#############
# RSS Feeds #
#############
feeds = toml.load(stage)["rss_feeds"]

rss_feed = feeds["links"]
