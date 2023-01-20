import toml

############
#  Server  #
############
toml_data = toml.load("Resources/server.toml")

server_info = toml_data["server"]["info"]

############
# Channels #
############
channels = toml_data["channels"]

mod_channel = channels["moderation"]
log_channel = channels["log_channel"]
normal_channel = channels["normal_channel"]

#############
#   Roles   #
#############
user_roles = toml_data["user_roles"]

admin_roles = user_roles["admin"]
elevated_roles = user_roles["elevated"]
badboi_role = user_roles["bad"]
unverified_role = user_roles["unverified"]
