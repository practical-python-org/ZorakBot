import toml
<<<<<<< HEAD

# Should probably find a place to put this in utilities.core, will leave it to you tho! - Masz


############
#  Server  #
############
toml_data = toml.load("Resources/server.toml")

server_info = toml_data["server"]["info"]
=======
prod = 'server.toml'
test = 'test_server.toml'
############
#  Server  #
############
server_info = toml.load(prod)['server']['info']
>>>>>>> Main

############
# Channels #
############
<<<<<<< HEAD
channels = toml_data["channels"]
=======
channels = toml.load(prod)['channels']
>>>>>>> Main

mod_channel = channels["moderation"]
log_channel = channels["log_channel"]
normal_channel = channels["normal_channel"]

#############
#   Roles   #
#############
<<<<<<< HEAD
user_roles = toml_data["user_roles"]
=======
user_roles = toml.load(prod)['user_roles']
>>>>>>> Main

admin_roles = user_roles["admin"]
elevated_roles = user_roles["elevated"]
badboi_role = user_roles["bad"]
unverified_role = user_roles["unverified"]
