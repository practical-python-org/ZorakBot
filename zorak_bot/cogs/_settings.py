import toml
test = '../../Resources/test_server.toml'
############
#  Server  #
############
server_info = toml.load('../../Resources/server.toml')['server']['info']

############
# Channels #
############
channels = toml.load('../../Resources/server.toml')['channels']

mod_channel = channels["moderation"]
log_channel = channels["log_channel"]
normal_channel = channels["normal_channel"]

#############
#   Roles   #
#############
user_roles = toml.load('../../Resources/server.toml')['user_roles']

admin_roles = user_roles["admin"]
elevated_roles = user_roles["elevated"]
badboi_role = user_roles["bad"]
unverified_role = user_roles["unverified"]
